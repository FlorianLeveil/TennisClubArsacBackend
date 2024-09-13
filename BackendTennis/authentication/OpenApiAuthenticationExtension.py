# Emplacement: BackendTennis/authentication/api_key_extension.py

from drf_spectacular.extensions import OpenApiAuthenticationExtension


class APIKeyAuthExtension(OpenApiAuthenticationExtension):
    target_class = 'BackendTennis.authentication.CustomAPIKeyAuthentication.CustomAPIKeyAuthentication'
    name = 'ApiKeyAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Api-Key',
            'description': 'API key required'
        }
