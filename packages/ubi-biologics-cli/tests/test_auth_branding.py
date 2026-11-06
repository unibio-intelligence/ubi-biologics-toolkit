import httpx

from ubi_cli.auth_branding import AuthBranding, FASTMCP_LOGO_URL


async def test_callback_branding_preserves_status_security_and_callback_script():
    body = ('<html><head><title>FastMCP OAuth</title></head><body>'
            f'<img alt="FastMCP" src="{FASTMCP_LOGO_URL}">'
            '<script>window.close()</script></body></html>').encode()

    async def callback(scope, receive, send):
        await send({"type": "http.response.start", "status": 400, "headers": [
            (b"content-type", b"text/html; charset=utf-8"),
            (b"cache-control", b"no-store"),
            (b"content-security-policy", b"default-src 'none'"),
            (b"content-length", str(len(body)).encode()),
        ]})
        await send({"type": "http.response.body", "body": body})

    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=AuthBranding(callback)), base_url="http://127.0.0.1") as client:
        response = await client.get("/callback")
    assert response.status_code == 400
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["content-security-policy"] == "default-src 'none'"
    assert int(response.headers["content-length"]) == len(response.content)
    assert '<script>window.close()</script>' in response.text
    assert 'alt="Ubi"' in response.text and 'data:image/png;base64,' in response.text
    assert FASTMCP_LOGO_URL not in response.text
