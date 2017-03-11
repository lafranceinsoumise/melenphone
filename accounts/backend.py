# coding: utf8
from __future__ import unicode_literals

from django.conf import settings
import requests
from requests.auth import AuthBase

from .models import User


class BearerTokenAuth(AuthBase):
    """Auth class used with requests to use Bearer token authentication

    To use Bearer token auth, the Authorization header must be set
    to the value of the token prefixed with "Bearer "
    """
    def __init__(self, access_token):
        self._access_token = access_token

    def __call__(self, r):
        r.headers['Authorization'] = "Bearer {}".format(self._access_token)
        return r


class JLMOAuth2(object):
    """Authentication backend that validates users using an access token from the JLM2017 OAuth provider

    Do not forget to add this backend to the AUTHENTICATION_BACKENDS settings.
    Set PROFILE_URL in the settings to the URI of the user validation API.

    Once it is configured, authenticating a user is as simple as calling authenticate(access_token=...)
    """
    def authenticate(self, access_token=None):
        if access_token:
            res = requests.get(settings.PROFILE_URL, auth=BearerTokenAuth(access_token))

            if res.status_code // 100 == 2:
                try:
                    profile = res.json()
                except ValueError:
                    # it was not JSON
                    return None

                email = profile.get('email', None)
                location = profile.get('location', {})
                city = location.get('city') or ''
                country_code = location.get('country_code') or ''
                if email:
                    user, created = User.objects.get_or_create(email=email, defaults={
                        'city': city,
                        'country_code': country_code
                    })
                    changed = False
                    if not created and not user.city:
                        user.city = city
                        changed = True
                    if not created and not user.country_code:
                        user.country_code = country_code
                        changed = True
                    if changed:
                        user.save()

                    return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
