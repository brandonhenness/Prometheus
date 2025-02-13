# dependencies.py
import os
import logging
import ldap3

from fastapi import Request, HTTPException, status

logger = logging.getLogger(__name__)


def get_current_user(request: Request) -> dict:
    """
    Combined dependency that accepts authentication via session or Kerberos.
    
    - If a session user is present, it uses that.
    - Otherwise, if Kerberos authentication info is available, it updates
      the session with the Kerberos user and uses that.
    - If neither is present, it raises a 401 Unauthorized.
    """
    # Check for session-based authentication first.
    session = getattr(request.state, "session", None)
    if session:
        user = session.get("user")
        if user:
            logger.debug(f"Authenticated via session: {user}")
            # You can return a simplified dictionary or full details.
            return {"upn": user}
    
    # Fall back to Kerberos-based authentication.
    auth_info = getattr(request.state, "auth_info", None)
    if auth_info:
        logger.debug(f"Authenticated via Kerberos: {auth_info}")
        # Optionally, update the session with Kerberos auth info for future requests.
        if session is not None:
            session["user"] = auth_info.get("upn")
        return auth_info

    logger.warning("Authentication required but no auth info found in session or Kerberos.")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Negotiate"},
    )


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
