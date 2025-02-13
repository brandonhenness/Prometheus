import json
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RedisSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cookie_name: str = "session", max_age: int = 3600):
        """
        Middleware that uses Redis to store session data.
        """
        super().__init__(app)
        self.cookie_name = cookie_name
        self.max_age = max_age

    async def dispatch(self, request: Request, call_next):
        # Get the Redis client from app state
        redis_client = request.app.state.redis

        # Retrieve session data using the session ID from the cookie (if available)
        session_id = request.cookies.get(self.cookie_name)
        if session_id:
            session_data = await redis_client.get(session_id)
            if session_data:
                request.state.session = json.loads(session_data)
            else:
                request.state.session = {}
        else:
            request.state.session = {}

        # Process the request
        response = await call_next(request)

        # Ensure a session ID exists; if not, create one and set it in a cookie
        session_id = request.cookies.get(self.cookie_name)
        if not session_id:
            session_id = str(uuid.uuid4())
            response.set_cookie(
                self.cookie_name,
                session_id,
                max_age=self.max_age,
                httponly=True,
            )
        # Save (or update) the session data in Redis with an expiration time
        await redis_client.set(session_id, json.dumps(request.state.session), ex=self.max_age)
        return response