# app/utils/cookies.py

from fastapi import Response

def set_user_auth_cookie(response: Response, user: dict):
    response.set_cookie(
        key="userAuth",
        value=user["upn"],
        path="/",
        httponly=True,
        secure=True,
        samesite="Lax",
        domain=".prometheus.osn.wa.gov",  # Consider making this configurable
    )
