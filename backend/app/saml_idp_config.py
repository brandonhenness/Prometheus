# saml2_idp_config.py

IDP_CONFIG = {
    "entityid": "https://api.prometheus.osn.wa.gov/saml/sso",  # The entity ID for your IdP
    "service": {
        "idp": {
            "authn_requests_signed": True,
            "want_authn_requests_signed": True,
            # The IdP “endpoints” define where the SP sends requests (SingleSignOnService) 
            # and where you handle Single Logout, if implemented
            "endpoints": {
                "single_sign_on_service": [
                    ("https://api.prometheus.osn.wa.gov/saml/sso", "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"),
                ],
                "single_logout_service": [
                    ("https://api.prometheus.osn.wa.gov/saml/slo", "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"),
                ],
            },
            "policy": {
                "default": {
                    "lifetime": {"minutes": 30},
                    "attribute_restrictions": None,  # release all attributes you have
                    "name_form": "urn:oasis:names:tc:SAML:2.0:attrname-format:uri",
                }
            }
        }
    },
    # The IdP typically needs a key to sign assertions
    "key_file": "/etc/saml/idp-key.pem",
    "cert_file": "/etc/saml/idp-cert.pem",
    "security": {
        "signature_algorithm": "http://www.w3.org/2001/04/xmldsig-more#rsa-sha256",
        "digest_algorithm": "http://www.w3.org/2001/04/xmlenc#sha256",
        "response_signed": True,
        "assertion_signed": True,
    },
    "debug": 1,
}
