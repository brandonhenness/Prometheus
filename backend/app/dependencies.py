# dependencies.py
import os
import base64
import logging
import traceback
import gssapi
import ldap3

from fastapi import Request, HTTPException, status

logger = logging.getLogger(__name__)

def requires_auth(request: Request) -> str:
    """
    A FastAPI dependency that ensures the request is authenticated
    via Kerberos. Raises HTTP 401 if not authenticated.
    """
    if not request.state.principal:
        logger.warning("Authentication required but principal is missing.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Negotiate"},
        )
    logger.debug(f"Request authenticated as: {request.state.principal}")
    return request.state.principal


def get_user_permissions_from_ad(user_info: str):
    """
    Example function that checks the user's AD groups and returns
    permissions, e.g. ["read", "admin"] if in MyAppAdmins group.
    """
    LDAP_SERVER = os.getenv("LDAP_SERVER")
    LDAP_USER = os.getenv("LDAP_USER")
    LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")
    LDAP_DOMAIN = os.getenv("LDAP_DOMAIN")

    user_permissions = ["read"]
    user_account = user_info.split("@")[0]

    try:
        server = ldap3.Server(LDAP_SERVER, get_info=ldap3.ALL)
        conn = ldap3.Connection(server, LDAP_USER, LDAP_PASSWORD, auto_bind=True)
    except Exception as e:
        logger.error(f"LDAP connection error: {e}")
        return user_permissions

    search_filter = f"(|(sAMAccountName={user_account})(userPrincipalName={user_info}))"
    try:
        conn.search(
            search_base=LDAP_DOMAIN,
            search_filter=search_filter,
            attributes=["memberOf"],
        )
    except Exception as e:
        logger.error(f"LDAP search error: {e}")
        return user_permissions

    if not conn.entries:
        return user_permissions

    user_entry = conn.entries[0]
    group_dns = user_entry.memberOf.values if "memberOf" in user_entry else []

    for group_dn in group_dns:
        if "MyAppAdmins" in group_dn:
            user_permissions.append("admin")

    return user_permissions
