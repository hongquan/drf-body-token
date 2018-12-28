"""
Authentication classes for REST.
"""
from typing import Optional

from django.conf import settings
from rest_framework.request import Request
from rest_framework.authentication import TokenAuthentication


AuthResult = Optional[tuple]
SETTINGS_KEY = 'DRF_BODY_TOKEN_FIELD'
DEFAULT_FIELD_NAME = 'access_token'


class BodyTokenAuthentication(TokenAuthentication):
    '''Accept token in HTTP body. The field name is configurable, default is "access_token"'''
    def authenticate(self, request: Request) -> AuthResult:
        field_name = getattr(settings, SETTINGS_KEY, DEFAULT_FIELD_NAME)
        key = request.data.get(field_name)
        if key:
            key = key.strip()
        # Skip if key is empty
        if not key:
            return None
        return self.authenticate_credentials(key)
