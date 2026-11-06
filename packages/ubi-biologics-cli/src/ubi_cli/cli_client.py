"""Maintained public Ubi native-client metadata; no registration credentials."""

IDENTITY_SCOPES = ('openid', 'email', 'profile')

CLIENT_PATH = "/.well-known/ubi-cli-client.json"
CALLBACK_PORT = 8765


def client_document(base, scopes=IDENTITY_SCOPES):
    return {
        "client_id": base.rstrip("/") + CLIENT_PATH,
        "client_name": "Ubi CLI",
        "application_type": "native",
        "redirect_uris": [f"http://127.0.0.1:{CALLBACK_PORT}/callback"],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "token_endpoint_auth_method": "none",
        "scope": " ".join(scopes),
    }
