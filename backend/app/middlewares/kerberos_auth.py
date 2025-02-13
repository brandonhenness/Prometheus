# middlewares/kerberos.py
import logging
import os
import base64
import traceback
import gssapi

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)

class KerberosAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.debug("Starting Kerberos authentication middleware dispatch.")

        # Set default authentication info to None so that it's falsy.
        request.state.auth_info = None

        auth_header = request.headers.get("Authorization")
        logger.debug(f"Authorization header: {auth_header}")
        if auth_header and auth_header.startswith("Negotiate "):
            spnego_token = auth_header[len("Negotiate "):].strip()
            logger.debug(f"Extracted SPNEGO token: {spnego_token}")

            try:
                service_principal = (
                    f'{os.getenv("KRB_SERVICE")}'
                    f'/{os.getenv("KRB_HOST")}@{os.getenv("KRB_REALM")}'
                )
                logger.debug(f"Using service principal: {service_principal}")

                # Create server credentials (usage="accept")
                server_creds = gssapi.Credentials(usage="accept")
                # Create a security context for accepting the token
                sec_context = gssapi.SecurityContext(creds=server_creds, usage="accept")

                # Decode the incoming SPNEGO token (Base64)
                in_token = base64.b64decode(spnego_token)
                logger.debug("Calling SecurityContext.step() with the incoming token.")
                out_token = sec_context.step(in_token)
                logger.debug(f"SecurityContext.step() returned: {out_token}")

                if sec_context.complete:
                    # Get the raw UPN (e.g., john.doe@example.com)
                    upn = str(sec_context.initiator_name).lower()

                    # Compute WindowsDomainQualifiedName:
                    if "@" in upn:
                        username, domain = upn.split("@", 1)
                        # Optionally, use an environment variable for the short domain:
                        short_domain = os.getenv("KRB_WINDOWS_DOMAIN", domain.split('.')[0])
                        wdqn = f"{short_domain.upper()}\\{username}"
                    else:
                        wdqn = upn

                    # Store the authentication details in request.state.auth_info
                    request.state.auth_info = {
                        "upn": upn,
                        "wdqn": wdqn,
                    }
                    logger.info(f"Authentication complete. Auth info: {request.state.auth_info}")
                else:
                    # Authentication is not complete; send back token if available.
                    out_token_b64 = (
                        base64.b64encode(out_token).decode("ascii") if out_token else ""
                    )
                    logger.warning("Authentication incomplete; additional token exchange required.")
                    return Response(
                        status_code=401,
                        headers={"WWW-Authenticate": f"Negotiate {out_token_b64}"},
                    )
            except Exception as e:
                logger.error(f"Kerberos error: {e}")
                logger.debug(traceback.format_exc())
                return Response(
                    status_code=401,
                    headers={"WWW-Authenticate": "Negotiate"},
                )
        else:
            logger.debug("No valid Negotiate Authorization header found.")

        response = await call_next(request)
        logger.debug("Exiting Kerberos authentication middleware dispatch.")
        return response
    