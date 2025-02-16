# middlewares/attach_cookie.py
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request

class AttachAuthCookieMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        # For lifespan events, simply pass them along.
        if scope["type"] == "lifespan":
            await self.app(scope, receive, send)
            return

        # Create a request instance to access request.state.
        request = Request(scope, receive=receive)

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # Check if the user was attached to the request state in a dependency.
                user = getattr(request.state, "user", None)
                if user is not None:
                    # Build the Set-Cookie header value.
                    cookie_value = user["upn"]
                    cookie_header = (
                        f"userAuth={cookie_value}; Path=/; HttpOnly; "
                        "Secure; SameSite=Lax; Domain=.prometheus.osn.wa.gov"
                    )
                    headers = message.get("headers", [])
                    headers.append((b"set-cookie", cookie_header.encode("latin-1")))
                    message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_wrapper)
