from rest_framework import authentication
from rest_framework import exceptions
from rest_framework_api_key.models import APIKey
import logging

logger = logging.getLogger(__name__)


class CustomAPIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Api-Key')
        if not api_key:
            logger.debug('No API Key provided in headers')
            raise exceptions.AuthenticationFailed('API Key is required')

        try:
            key = APIKey.objects.get_from_key(api_key)
            if key.revoked:
                logger.debug('API Key is revoked')
                raise exceptions.AuthenticationFailed('API Key inactive or deleted')
        except APIKey.DoesNotExist:
            logger.debug('API Key does not exist')
            raise exceptions.AuthenticationFailed('Invalid API Key')

        logger.debug('API Key is valid and active')
        return None, None
