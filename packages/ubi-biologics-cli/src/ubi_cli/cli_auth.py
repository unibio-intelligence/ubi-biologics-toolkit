"""Resource-bound native CLI OAuth; no DCR or plaintext credential fallback."""

from __future__ import annotations

import hashlib
import logging
import os
import time
import webbrowser
from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import anyio
import httpx2
import keyring
from fastmcp.client.auth import OAuth
from fastmcp.client.auth.oauth import TokenStorageAdapter
from fastmcp.client.oauth_callback import (
    OAuthCallbackResult,
    create_oauth_callback_server,
)
from key_value.aio._utils.compound import compound_key
from key_value.aio.stores.keyring import KeyringStore
from key_value.aio.stores.keyring.store import (
    KeyringV1CollectionSanitizationStrategy,
    KeyringV1KeySanitizationStrategy,
)
from keyring.errors import PasswordDeleteError
from mcp.client.auth import AuthorizationCodeResult
from .auth_branding import AuthBranding
from .errors import ServiceError

from .cli_client import CALLBACK_PORT, CLIENT_PATH


def resource_url(value):
    """Validate before constructing a transport or forwarding any credential."""
    try:
        if (
            not isinstance(value, str)
            or len(value) > 2048
            or any(c.isspace() or ord(c) < 32 for c in value)
            or "\\" in value
        ):
            raise ValueError
        parsed = urlsplit(value)
        local = (
            os.getenv("UBI_PROFILE") == "local"
            and parsed.hostname in {"127.0.0.1", "localhost", "::1"}
            and parsed.scheme == "http"
        )
        if (
            not parsed.hostname
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
            or (parsed.scheme != "https" and not local)
            or "%" in parsed.netloc
        ):
            raise ValueError
        port = parsed.port
        host = parsed.hostname.lower()
        if ":" in host:
            host = f"[{host}]"
        authority = host + (
            f":{port}"
            if port is not None and not (port == 443 and parsed.scheme == "https")
            else ""
        )
        path = parsed.path.rstrip("/")
        if not path or any(part in {".", ".."} for part in path.split("/")):
            raise ValueError
        return urlunsplit((parsed.scheme, authority, path, "", ""))
    except (ValueError, TypeError):
        raise ServiceError(
            "invalid_resource_url",
            "Use a canonical HTTPS MCP URL without credentials, query or fragment. HTTP is allowed only for loopback in UBI_PROFILE=local.",
        ) from None


def base_url(resource):
    if not resource.endswith("/mcp"):
        raise ServiceError(
            "invalid_resource_url", "Ubi OAuth resources must end in /mcp."
        )
    return resource[:-4]


@dataclass(frozen=True)
class NativeClient:
    identity: str
    metadata_url: str | None
    callback_port: int

    @classmethod
    def configured(cls, resource):
        static = os.getenv("UBI_CLI_CLIENT_ID", "")
        metadata = os.getenv("UBI_CLI_CLIENT_METADATA_URL", "")
        try:
            port = int(os.getenv("UBI_CLI_CALLBACK_PORT", str(CALLBACK_PORT)))
        except ValueError:
            raise ServiceError(
                "invalid_cli_client",
                "The callback port must be an integer from 1024 to 65535.",
            ) from None
        if not 1024 <= port <= 65535 or (static and metadata):
            raise ServiceError(
                "invalid_cli_client",
                "Configure exactly one CIMD URL or reviewed static client ID and a loopback callback port.",
            )
        if static:
            if (
                not 1 <= len(static) <= 256
                or ":" in static
                or any(c.isspace() or ord(c) < 32 for c in static)
            ):
                raise ServiceError(
                    "invalid_cli_client",
                    "Use the exact approved opaque native client ID.",
                )
            return cls(static, None, port)
        if not metadata:
            if port != CALLBACK_PORT:
                raise ServiceError(
                    "invalid_cli_client",
                    "The maintained Ubi CLI document requires callback port 8765. A custom port needs an explicitly reviewed client identity.",
                )
            metadata = base_url(resource) + CLIENT_PATH
        checked = resource_url(metadata)
        if (
            urlsplit(checked).scheme != "https"
            or checked != metadata
            or not urlsplit(checked).path.strip("/")
        ):
            raise ServiceError(
                "invalid_cli_client",
                "The CIMD identity must be an exact HTTPS document URL.",
            )
        return cls(metadata, metadata, port)


class SecureKeyringStore(KeyringStore):
    def __init__(self, resource, identity):
        backend = keyring.get_keyring()
        approved = {
            ("keyring.backends.macOS", "Keyring"),
            ("keyring.backends.SecretService", "Keyring"),
            ("keyring.backends.Windows", "WinVaultKeyring"),
        }
        if (type(backend).__module__, type(backend).__name__) not in approved:
            raise ServiceError(
                "credential_store_unavailable",
                "Unlock a supported OS keyring (macOS, Secret Service or Windows Credential Manager), or use UBI_MCP_TOKEN for headless calls.",
            )
        self.backend = backend
        namespace = hashlib.sha256((resource + "\0" + identity).encode()).hexdigest()
        super().__init__(
            service_name="Ubi CLI:" + namespace,
            key_sanitization_strategy=KeyringV1KeySanitizationStrategy(),
            collection_sanitization_strategy=KeyringV1CollectionSanitizationStrategy(),
        )

    def _warn_about_stability(self):
        # This CLI wrapper pins the backend version and verifies its storage
        # contract. Keep library implementation warnings out of JSON stderr.
        pass

    def _username(self, key, collection):
        return compound_key(
            collection=self._sanitize_collection(collection=collection),
            key=self._sanitize_key(key=key),
        )

    async def _get_managed_entry(self, *, key, collection):
        try:
            raw = self.backend.get_password(
                self._service_name, self._username(key, collection)
            )
            if raw is None:
                return None
            if len(raw.encode()) > 65536:
                raise ValueError
            return self._serialization_adapter.load_json(json_str=raw)
        except Exception:  # noqa: BLE001 — redact backend failures and credential contents
            raise ServiceError(
                "credential_store_unavailable",
                "The OS keyring entry cannot be read safely. Unlock the keyring or remove this resource's saved credentials.",
            ) from None

    async def _put_managed_entry(self, *, key, collection, managed_entry):
        try:
            raw = self._serialization_adapter.dump_json(
                entry=managed_entry, key=key, collection=collection
            )
            if len(raw.encode()) > 65536:
                raise ValueError
            self.backend.set_password(
                self._service_name, self._username(key, collection), raw
            )
        except Exception:  # noqa: BLE001 — redact backend failures and credential contents
            raise ServiceError(
                "credential_store_unavailable",
                "The OS keyring could not save credentials; no plaintext fallback is used.",
            ) from None

    async def _delete_managed_entry(self, *, key, collection):
        try:
            self.backend.delete_password(
                self._service_name, self._username(key, collection)
            )
            return True
        except PasswordDeleteError:
            return False
        except Exception:  # noqa: BLE001 — redact backend failures and credential contents
            raise ServiceError(
                "credential_store_unavailable",
                "The OS keyring could not remove this resource's credentials.",
            ) from None


def http_factory(resource):
    # HTTP info/trace logs can include OAuth query state and cookie headers.
    # The CLI reports connection failures through its safe JSON boundary.
    logging.getLogger("httpx2").disabled = True
    logging.getLogger("httpcore2").setLevel(logging.CRITICAL + 1)
    for name in tuple(logging.Logger.manager.loggerDict):
        if name.startswith("httpcore2."):
            logging.getLogger(name).disabled = True
    origin = urlsplit(resource)

    async def guard(request):
        # Ubi is its own authorization server. Metadata cannot redirect native
        # credentials to a different authority or cleartext endpoint.
        destination = resource_url(str(request.url).split("?", 1)[0])
        target = urlsplit(destination)
        if (target.scheme, target.netloc) != (origin.scheme, origin.netloc):
            raise ServiceError(
                "oauth_endpoint_denied",
                "OAuth and MCP requests must remain on the configured Ubi resource origin.",
            )
        if request.method == "POST" and request.url.path.endswith("/register"):
            raise ServiceError(
                "dcr_disabled", "Ubi CLI does not perform dynamic client registration."
            )

    def factory(**kwargs):
        hooks = kwargs.pop("event_hooks", {})
        kwargs["event_hooks"] = {**hooks, "request": [guard, *hooks.get("request", [])]}
        kwargs["follow_redirects"] = False
        kwargs.setdefault("timeout", 15)
        return httpx2.AsyncClient(**kwargs)

    return factory


class NativeOAuth(OAuth):
    def __init__(self, resource, client, storage, *, interactive):
        # Foreign SDK exception logs can include token response bodies. Native
        # CLI errors are deliberately mapped to safe JSON at the outer boundary.
        logging.getLogger("mcp.client.auth.oauth2").disabled = True
        logging.getLogger("fastmcp.client.auth.oauth").disabled = True
        self.interactive = interactive
        # Supplying the exact identity as static information prevents the SDK's
        # CIMD-to-DCR fallback even when metadata advertises no CIMD support.
        super().__init__(
            resource,
            client_name="Ubi CLI",
            client_id=client.identity,
            client_metadata_url=client.metadata_url,
            callback_host="127.0.0.1",
            callback_port=client.callback_port,
            callback_timeout=180,
            # The resource selects its configured identity scopes. AWS OAuth-only
            # deployments deliberately exclude openid; requesting it breaks login.
            scopes=None,
            additional_client_metadata={
                "application_type": "native",
                "token_endpoint_auth_method": "none",
            },
            token_storage=storage,
            httpx_client_factory=http_factory(resource),
        )

    async def callback_handler(self):
        # Retain the pinned SDK's callback parsing, first-response fence and
        # issuer capture; only wrap the generated HTML presentation.
        result = OAuthCallbackResult()
        ready = anyio.Event()
        server = create_oauth_callback_server(
            port=self.redirect_port,
            host=self._callback_host,
            server_url=self.mcp_url,
            result_container=result,
            result_ready=ready,
        )
        server.config.app = AuthBranding(server.config.app)
        async with anyio.create_task_group() as group:
            group.start_soon(server.serve)
            try:
                with anyio.fail_after(self._callback_timeout):
                    await ready.wait()
                    if result.error is not None:
                        raise result.error
                    if result.code is None:
                        raise ServiceError("login_failed")
                    return AuthorizationCodeResult(
                        code=result.code, state=result.state, iss=result.iss
                    )
            finally:
                server.should_exit = True
                await anyio.sleep(0.1)
                group.cancel_scope.cancel()

    def _bound_token_request(self, request):
        fields = dict(parse_qsl(request.content.decode(), keep_blank_values=True))
        if (
            fields.get("resource", self.mcp_url) != self.mcp_url
            or fields.get("client_id") != self._client_id
        ):
            raise ServiceError(
                "oauth_resource_mismatch",
                "The token request does not match this resource and native client.",
            )
        fields["resource"] = self.mcp_url
        return httpx2.Request(
            request.method,
            request.url,
            headers={
                k: v
                for k, v in request.headers.items()
                if k.lower() != "content-length"
            },
            content=urlencode(fields).encode(),
            extensions=request.extensions,
        )

    async def _refresh_token(self):
        # New processes have no PRM in SDK memory yet; refresh must still include
        # the resource to which the persisted grant and this store are bound.
        return self._bound_token_request(await super()._refresh_token())

    async def _exchange_token_authorization_code(self, auth_code, code_verifier):
        return self._bound_token_request(
            await super()._exchange_token_authorization_code(auth_code, code_verifier)
        )

    async def redirect_handler(self, authorization_url):
        if not self.interactive:
            raise ServiceError(
                "login_required",
                "Run ubi-biologics-cli login to authorize this resource and client.",
            )
        async with self.httpx_client_factory() as client:
            response = await client.get(authorization_url)
        if response.status_code not in {200, 302, 303, 307, 308}:
            raise ServiceError(
                "client_not_approved",
                "The resource rejected this native client. Check the reviewed client identity and exact loopback redirect.",
            )
        if not webbrowser.open(authorization_url):
            raise ServiceError(
                "browser_unavailable", "A browser could not be opened for OAuth login."
            )


async def credential_status(resource, client, store):
    adapter = TokenStorageAdapter(store, resource)
    tokens = await adapter.get_tokens()
    expiry = await adapter.get_token_expiry()
    return {
        "resource": resource,
        "client_id": client.identity,
        "credential_store": "os_keyring",
        "tokens_present": tokens is not None,
        "access_expired": bool(expiry is not None and expiry <= time.time())
        if tokens
        else None,
        "refresh_available": bool(tokens and tokens.refresh_token),
        "expires_at": expiry if tokens else None,
        "server_authorization_checked": False,
    }


async def revoke(resource, client, store, *, forget_local=False, logout=False):
    adapter = TokenStorageAdapter(store, resource)
    tokens = await adapter.get_tokens()
    if not forget_local and tokens:
        async with http_factory(resource)() as http:
            response = await http.post(
                base_url(resource) + "/revoke",
                data={
                    "token": tokens.refresh_token or tokens.access_token,
                    "token_type_hint": "refresh_token"
                    if tokens.refresh_token
                    else "access_token",
                    "client_id": client.identity,
                },
            )
        if response.status_code != 200:
            raise ServiceError(
                "revocation_failed",
                "Server revocation was not confirmed; saved credentials remain available for another attempt.",
                retryable=True,
            )
    if logout or forget_local:
        await adapter.clear()
    else:
        await store.delete(resource + "/tokens", collection="mcp-oauth-token")
        await store.delete(
            resource + "/token_expiry", collection="mcp-oauth-token-expiry"
        )
    return {
        "resource": resource,
        "local_credentials_removed": True,
        "server_revoked": bool(tokens and not forget_local),
        "server_grants_may_remain": bool(forget_local),
    }
