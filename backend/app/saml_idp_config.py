# saml2_idp_config.py
#TODO: Possibly move this to an actual config file
from saml2 import BINDING_HTTP_REDIRECT

IDP_CONFIG = {
    "debug": True,
    "entityid": "https://prometheus.osn.wa.gov/api/saml/metadata",
    "service": {
        "idp": {
            "name_id_format": "urn:oasis:names:tc:SAML:1.1:nameid-format:WindowsDomainQualifiedName",
            "authn_requests_signed": True,
            "want_authn_requests_signed": False, #TODO: Look into enabling this
            "sign_response": True,
            "sign_assertion": True,
            # The IdP “endpoints” define where the SP sends requests (SingleSignOnService) 
            # and where you handle Single Logout, if implemented
            "endpoints": {
                "single_sign_on_service": [
                    (
                        "https://prometheus.osn.wa.gov/api/saml/sso", 
                        BINDING_HTTP_REDIRECT,
                     ),
                ],
                "single_logout_service": [
                    (
                        "https://prometheus.osn.wa.gov/api/saml/slo",
                        BINDING_HTTP_REDIRECT,
                    ),
                ],
            },
            "policy": {
                # the policy for all services
                "default": {
                    "lifetime": {"minutes":15},
                    "attribute_restrictions": None,
                    "persistent_name_id": False,
                    "entity_categories": ["edugain"],
                    "attributes": {
                        "email": "user.email",
                        "first_name": "user.first_name",
                        "last_name": "user.last_name",
                    },
                },
            }
        }
    },
    "key_file": "/etc/ssl/private/idp-key.pem",
    "cert_file": "/etc/ssl/certs/idp-cert.pem",
    "security": {
        "signature_algorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
        "digest_algorithm": "http://www.w3.org/2001/04/xmlenc#sha256",
        "response_signed": True,
        "assertion_signed": True,
    },
    "debug": 1,
    "metadata": {
        "remote": [
            {
                "url": "https://canvas.prometheus.osn.wa.gov/saml2",
            }
        ]
    },
}
