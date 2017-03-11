# coding: utf8
from __future__ import unicode_literals

from django.conf import settings
from django.views.generic import RedirectView
from django.urls import reverse_lazy
from django.utils.translation import string_concat
from django.utils.crypto import get_random_string
from django.http import HttpResponseBadRequest

from django.contrib.auth import authenticate, login

import logging

logger = logging.getLogger(__name__)

from oauth2client.client import OAuth2WebServerFlow

flow = OAuth2WebServerFlow(
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    scope=settings.DEFAULT_SCOPE,
    auth_uri=settings.AUTHORIZATION_URL,
    token_uri=settings.ACCESS_TOKEN_URL,
    # use reverse_lazy and string_concat because the resolver is not ready when initializing this
    redirect_uri=string_concat(settings.REDIRECT_BASE.rstrip('/'), reverse_lazy('accounts:oauth_callback'))
)
"""Flow instance responsible for handling the OAuth2 process

The following settings parameters are required:

* CLIENT_ID: the client id used to authenticate oneself with the OAuth2 provider
* CLIENT_SECRET: the client secret used to authenticate oneself with the OAuth2 provider
* DEFAULT_SCOPE: the scope to ask for during the OAuth2 process
* AUTHORIZATION_URL: the url of the authorization endpoint to redirect to during step 1 of the process
* ACCESS_TOKEN_URL: the url of the token endpoint to which a POST request is made to get the access token
* REDIRECT_BASE: the base URL to which the OAuth2 endpoint must redirect
"""


class RedirectToAuthProvider(RedirectView):
    """Starts up the OAuth2 process by redirecting the user to the OAuth2 provider

    The URL to which the user is redirected is build using the flow instance defined above
    """
    http_method_names = ['get']

    def get_redirect_url(self, *args, **kwargs):

        state_nonce = get_random_string(32)

        self.request.session['oauth2_nonce'] = state_nonce
        return flow.step1_get_authorize_url(state=state_nonce)


class AuthReturn(RedirectView):
    """OAuth2 callback view implementing step 2 of OAuth2

    This view is normally accessed only during the OAuth2 process, when the OAuth2
    provider redirects the user back to our website.

    It verifies the parameters returned by the OAuth2 provider are correct and executes
    step 2 of the OAuth2 process, getting back the access token from the token exchange
    endpoint.

    It then tries to authenticate the user using that same access token and log her in
    if it worked, before redirecting the user back to the main page.
    """
    http_method_names = ['get']
    url = reverse_lazy(settings.LOGIN_REDIRECT)

    def get(self, request, *args, **kwargs):
        state_nonce = request.session.get('oauth2_nonce', None)
        if not state_nonce or request.GET.get('state') != state_nonce:
            return HttpResponseBadRequest(b'Bad state')

        credentials = flow.step2_exchange(request.GET)
        access_token = credentials.get_access_token().access_token

        user = authenticate(access_token=access_token)

        if user:
            user.access_token = access_token
            user.save()
            login(request, user)
        else:
            return HttpResponseBadRequest(b'Did not get profile')

        # delete nonce so that the redirect cannot be done twice
        del request.session['oauth2_nonce']

        return super(AuthReturn, self).get(request, *args, **kwargs)
