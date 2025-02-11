# middlewares/kerberos_auth.py
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
        request.state.principal = None

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
                    principal = str(sec_context.initiator_name)
                    request.state.principal = principal
                    logger.info(f"Authentication complete. Principal: {principal}")
                else:
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
        else:
            logger.debug("No valid Negotiate Authorization header found.")

        response = await call_next(request)
        logger.debug("Exiting Kerberos authentication middleware dispatch.")
        return response
