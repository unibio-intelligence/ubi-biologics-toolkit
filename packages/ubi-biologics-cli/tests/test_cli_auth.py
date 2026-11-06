"""Native CLI onboarding and resource isolation without live credentials/keyrings."""
import hashlib
import json
import time
from urllib.parse import parse_qs, urlsplit
import httpx
import httpx2
import pytest
from fastmcp.client.auth.oauth import TokenStorageAdapter
from keyring.errors import PasswordDeleteError
from mcp.shared.auth import AuthorizationCodeResult, OAuthToken
from ubi_cli.errors import ServiceError
from ubi_cli import cli_auth
from ubi_cli.cli_auth import NativeClient, NativeOAuth, SecureKeyringStore
from ubi_cli.cli_client import CLIENT_PATH, client_document
RESOURCE = 'https://platform.example/mcp'

@pytest.fixture
async def keyring_backend(monkeypatch):

    class Keyring:
        __module__ = 'keyring.backends.macOS'

        def __init__(self):
            self.entries = {}
            self.locked = False

        def get_password(self, service, username):
            if self.locked:
                raise RuntimeError('private credential backend error')
            return self.entries.get((service, username))

        def set_password(self, service, username, value):
            if self.locked:
                raise RuntimeError('private credential backend error')
            self.entries[service, username] = value

        def delete_password(self, service, username):
            if self.locked:
                raise RuntimeError('private credential backend error')
            if (service, username) not in self.entries:
                raise PasswordDeleteError()
            del self.entries[service, username]
    backend = Keyring()
    monkeypatch.setattr(cli_auth.keyring, 'get_keyring', lambda: backend)
    for name in ('UBI_CLI_CLIENT_ID', 'UBI_CLI_CLIENT_METADATA_URL', 'UBI_CLI_CALLBACK_PORT', 'UBI_MCP_TOKEN'):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv('UBI_PROFILE', 'hosted')
    return backend

@pytest.mark.parametrize('url', ['http://platform.example/mcp', 'http://127.0.0.1/mcp', 'https://user:password@platform.example/mcp', 'https://user@platform.example/mcp', 'https://platform.example/mcp?token=private', 'https://platform.example/mcp#fragment', 'https://platform.example:bad/mcp', 'https://platform.example/../mcp', 'https://platform.example\\@evil.example/mcp', 'https://platform.example/mcp\n', 'file:///mcp', 'https://%70latform.example/mcp'])
async def test_invalid_url_rejected_before_any_credential_or_transport_access(url, monkeypatch):
    from ubi_cli.cli import call
    monkeypatch.setenv('UBI_PROFILE', 'hosted')
    monkeypatch.setenv('UBI_MCP_TOKEN', 'synthetic-secret')
    with pytest.raises(ServiceError) as error:
        await call('quota', {}, url=url)
    assert error.value.code == 'invalid_resource_url'
    assert 'password' not in str(error.value) and 'synthetic-secret' not in str(error.value)

def test_loopback_http_requires_explicit_local_profile(monkeypatch):
    monkeypatch.setenv('UBI_PROFILE', 'local')
    assert cli_auth.resource_url('http://127.0.0.1:8000/mcp') == 'http://127.0.0.1:8000/mcp'
    assert cli_auth.resource_url('http://[::1]:8000/mcp') == 'http://[::1]:8000/mcp'
    with pytest.raises(ServiceError):
        cli_auth.resource_url('http://private.example/mcp')
    assert cli_auth.resource_url('HTTPS://PLATFORM.EXAMPLE:443/mcp/') == RESOURCE

async def test_maintained_cimd_native_identity_and_static_configuration(keyring_backend, monkeypatch):
    client = NativeClient.configured(RESOURCE)
    assert client.identity == 'https://platform.example' + CLIENT_PATH
    auth = NativeOAuth(RESOURCE, client, SecureKeyringStore(RESOURCE, client.identity), interactive=False)
    assert auth._static_client_info.client_id == client.identity
    assert str(auth.context.client_metadata.redirect_uris[0]) == 'http://127.0.0.1:8765/callback'
    assert auth.context.client_metadata.token_endpoint_auth_method == 'none'
    monkeypatch.setenv('UBI_CLI_CALLBACK_PORT', '9000')
    with pytest.raises(ServiceError, match='maintained'):
        NativeClient.configured(RESOURCE)
    monkeypatch.setenv('UBI_CLI_CLIENT_ID', 'reviewed-native')
    custom = NativeClient.configured(RESOURCE)
    assert custom.identity == 'reviewed-native' and custom.callback_port == 9000
    monkeypatch.setenv('UBI_CLI_CLIENT_METADATA_URL', 'https://client.example/metadata.json')
    with pytest.raises(ServiceError):
        NativeClient.configured(RESOURCE)

async def test_keyring_persistence_scope_and_safe_status(keyring_backend):
    client = NativeClient.configured(RESOURCE)
    store = SecureKeyringStore(RESOURCE, client.identity)
    adapter = TokenStorageAdapter(store, RESOURCE)
    await adapter.set_tokens(OAuthToken(access_token='synthetic-access', refresh_token='synthetic-refresh', token_type='Bearer', expires_in=3600))
    status = await cli_auth.credential_status(RESOURCE, client, SecureKeyringStore(RESOURCE, client.identity))
    assert status['tokens_present'] and status['refresh_available'] and (not status['access_expired'])
    assert 'synthetic-access' not in json.dumps(status) and 'synthetic-refresh' not in json.dumps(status)
    assert not await TokenStorageAdapter(SecureKeyringStore(RESOURCE, 'other-client'), RESOURCE).get_tokens()
    other = 'https://other.example/mcp'
    assert not await TokenStorageAdapter(SecureKeyringStore(other, client.identity), other).get_tokens()
    keyring_backend.locked = True
    with pytest.raises(ServiceError) as error:
        await adapter.get_tokens()
    assert error.value.code == 'credential_store_unavailable' and 'private' not in str(error.value)

async def test_plaintext_or_missing_keyring_fails_closed(monkeypatch):
    monkeypatch.setattr(cli_auth.keyring, 'get_keyring', lambda: object())
    with pytest.raises(ServiceError, match='supported OS keyring'):
        SecureKeyringStore(RESOURCE, 'client')

async def test_origin_guard_rejects_credential_leak_and_dcr_before_transport(monkeypatch):
    hits = []

    async def handler(request):
        hits.append(request.url)
        return httpx2.Response(200, request=request)
    async with cli_auth.http_factory(RESOURCE)(transport=httpx2.MockTransport(handler)) as http:
        for url in ('https://evil.example/token', 'http://platform.example/token', 'https://platform.example/register'):
            with pytest.raises(ServiceError):
                await http.post(url, data={'refresh_token': 'synthetic-private'})
        assert not hits
        response = await http.post('https://platform.example/token', data={'grant_type': 'refresh_token'})
        assert response.status_code == 200 and len(hits) == 1

async def test_noninteractive_cli_cannot_open_browser(keyring_backend, monkeypatch):
    client = NativeClient.configured(RESOURCE)
    auth = NativeOAuth(RESOURCE, client, SecureKeyringStore(RESOURCE, client.identity), interactive=False)
    opened = []
    monkeypatch.setattr(cli_auth.webbrowser, 'open', lambda uri: opened.append(uri))
    with pytest.raises(ServiceError, match='ubi-biologics-cli login'):
        await auth.redirect_handler('https://platform.example/authorize')
    assert not opened

@pytest.mark.parametrize('identity_scopes', [['openid', 'email', 'profile'], ['email', 'profile']])
async def test_fresh_oauth_reconnect_refresh_and_revoke_without_dcr(keyring_backend, monkeypatch, identity_scopes):
    import base64
    client = NativeClient.configured(RESOURCE)
    requests, browser = ([], [])
    grants = {'access-one': True}
    resource_fields = []

    async def handler(request):
        path = request.url.path
        requests.append((request.method, path))
        if path == '/mcp':
            token = request.headers.get('Authorization', '').removeprefix('Bearer ')
            if grants.get(token):
                return httpx2.Response(200, json={'authorized': True}, request=request)
            return httpx2.Response(401, headers={'WWW-Authenticate': 'Bearer resource_metadata="https://platform.example/.well-known/oauth-protected-resource/mcp"'}, request=request)
        if path == '/.well-known/oauth-protected-resource/mcp':
            return httpx2.Response(200, json={'resource': RESOURCE, 'authorization_servers': ['https://platform.example'], 'scopes_supported': identity_scopes}, request=request)
        if path == '/.well-known/oauth-authorization-server':
            return httpx2.Response(200, json={'issuer': 'https://platform.example', 'authorization_endpoint': 'https://platform.example/authorize', 'token_endpoint': 'https://platform.example/token', 'registration_endpoint': 'https://platform.example/dynamic', 'response_types_supported': ['code'], 'grant_types_supported': ['authorization_code', 'refresh_token'], 'code_challenge_methods_supported': ['S256']}, request=request)
        if path == '/authorize':
            return httpx2.Response(302, headers={'Location': 'https://identity.example/login'}, request=request)
        if path == '/token':
            fields = parse_qs(request.content.decode())
            resource_fields.append(fields['resource'][0])
            assert fields['client_id'] == [client.identity]
            if fields['grant_type'] == ['authorization_code']:
                supplied = parse_qs(urlsplit(browser[-1]).query)
                assert supplied['scope'] == [' '.join(identity_scopes)]
                assert supplied['redirect_uri'] == ['http://127.0.0.1:8765/callback']
                expected = base64.urlsafe_b64encode(hashlib.sha256(fields['code_verifier'][0].encode()).digest()).decode().rstrip('=')
                assert supplied['code_challenge'] == [expected]
                return httpx2.Response(200, json={'access_token': 'access-one', 'refresh_token': 'refresh-one', 'token_type': 'Bearer', 'expires_in': 3600}, request=request)
            assert fields['refresh_token'] == ['refresh-one']
            grants['access-two'] = True
            return httpx2.Response(200, json={'access_token': 'access-two', 'refresh_token': 'refresh-two', 'token_type': 'Bearer', 'expires_in': 3600}, request=request)
        if path == '/revoke':
            fields = parse_qs(request.content.decode())
            assert fields['token'] == ['refresh-two'] and fields['client_id'] == [client.identity]
            grants.clear()
            return httpx2.Response(200, request=request)
        raise AssertionError('Unexpected request path')
    original_factory = cli_auth.http_factory

    def fixture_factory(resource):
        factory = original_factory(resource)
        return lambda **kw: factory(transport=httpx2.MockTransport(handler), **kw)
    monkeypatch.setattr(cli_auth, 'http_factory', fixture_factory)
    monkeypatch.setattr(cli_auth.webbrowser, 'open', lambda url: browser.append(url) or True)

    class FixtureOAuth(NativeOAuth):

        async def callback_handler(self):
            return AuthorizationCodeResult(code='fixture-code', state=parse_qs(urlsplit(browser[-1]).query)['state'][0])
    first_store = SecureKeyringStore(RESOURCE, client.identity)
    first = FixtureOAuth(RESOURCE, client, first_store, interactive=True)
    async with fixture_factory(RESOURCE)(auth=first) as http:
        assert (await http.get(RESOURCE)).status_code == 200
    assert len(browser) == 1
    adapter = TokenStorageAdapter(first_store, RESOURCE)
    await first_store.put(RESOURCE + '/token_expiry', {'expires_at': time.time() - 1}, collection='mcp-oauth-token-expiry')
    reconnected_store = SecureKeyringStore(RESOURCE, client.identity)
    second = FixtureOAuth(RESOURCE, client, reconnected_store, interactive=False)
    async with fixture_factory(RESOURCE)(auth=second) as http:
        assert (await http.get(RESOURCE)).status_code == 200
    assert (await adapter.get_tokens()).access_token == 'access-two'
    assert len(browser) == 1 and ('POST', '/dynamic') not in requests
    assert resource_fields == [RESOURCE, RESOURCE]
    result = await cli_auth.revoke(RESOURCE, client, reconnected_store, logout=True)
    assert result['server_revoked'] and (not await adapter.get_tokens())
    assert not await adapter.get_client_info()
    assert not (await cli_auth.credential_status(RESOURCE, client, reconnected_store))['tokens_present']

async def test_failed_revocation_preserves_credentials_and_local_forget_is_explicit(keyring_backend, monkeypatch):
    client = NativeClient.configured(RESOURCE)
    store = SecureKeyringStore(RESOURCE, client.identity)
    adapter = TokenStorageAdapter(store, RESOURCE)
    await adapter.set_tokens(OAuthToken(access_token='access', token_type='Bearer'))

    def factory(resource):
        return lambda **kw: httpx2.AsyncClient(transport=httpx2.MockTransport(lambda request: httpx2.Response(503, request=request)), **kw)
    monkeypatch.setattr(cli_auth, 'http_factory', factory)
    with pytest.raises(ServiceError, match='not confirmed'):
        await cli_auth.revoke(RESOURCE, client, store, logout=True)
    assert await adapter.get_tokens()
    removed = await cli_auth.revoke(RESOURCE, client, store, forget_local=True, logout=True)
    assert removed['server_grants_may_remain'] and (not removed['server_revoked'])
    assert not await adapter.get_tokens()

async def test_http_logs_never_emit_oauth_state_at_debug_level(caplog):
    import logging
    with caplog.at_level(logging.DEBUG, logger='httpx2'):
        async with cli_auth.http_factory(RESOURCE)(transport=httpx2.MockTransport(lambda request: httpx2.Response(302, request=request))) as http:
            await http.get('https://platform.example/authorize?state=synthetic-private-state')
    assert 'synthetic-private-state' not in caplog.text
