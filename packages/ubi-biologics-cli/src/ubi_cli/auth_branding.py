"""Apply bundled Ubi branding to SDK-generated authentication HTML only."""

import base64
from importlib.resources import files

from fastmcp.utilities.ui import FASTMCP_LOGO_URL

LOGO_MIME_TYPE = "image/png"
LOGO_URL = f"data:{LOGO_MIME_TYPE};base64," + base64.b64encode(
    files("ubi_cli").joinpath("assets/ubi-logo.png").read_bytes()
).decode("ascii")


def brand_auth_html(body: bytes) -> bytes:
    # Do not alter status messages, consent controls, scripts or security policy.
    # Both callback and error pages use the SDK's fixed logo URL.
    if FASTMCP_LOGO_URL.encode() not in body:
        return body
    return (
        body.replace(FASTMCP_LOGO_URL.encode(), LOGO_URL.encode())
        .replace(b'alt="FastMCP"', b'alt="Ubi"')
        .replace(b"<title>FastMCP OAuth</title>", b"<title>Ubi authentication</title>")
        .replace(b"</head>", f'<link rel="icon" href="{LOGO_URL}" /></head>'.encode())
    )


class AuthBranding:
    """Preserve the SDK auth handler and response security headers verbatim."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        start = None
        buffered = []
        size = 0

        async def branded_send(message):
            nonlocal start, size
            if message["type"] == "http.response.start":
                headers = dict(message.get("headers", []))
                if headers.get(b"content-type", b"").startswith(b"text/html"):
                    start = message
                    return
            elif message["type"] == "http.response.body" and start is not None:
                buffered.append(message)
                size += len(message.get("body", b""))
                if size > 256 * 1024:
                    # Authentication templates are small. Do not buffer another
                    # product page or change its streaming behavior indefinitely.
                    await send(start)
                    start = None
                    for chunk in buffered:
                        await send(chunk)
                    buffered.clear()
                    return
                if message.get("more_body", False):
                    return
                body = brand_auth_html(
                    b"".join(chunk.get("body", b"") for chunk in buffered)
                )
                headers = [
                    (key, value)
                    for key, value in start.get("headers", [])
                    if key != b"content-length"
                ]
                headers.append((b"content-length", str(len(body)).encode()))
                await send({**start, "headers": headers})
                await send({"type": "http.response.body", "body": body})
                start = None
                buffered.clear()
                return
            await send(message)

        await self.app(scope, receive, branded_send)
