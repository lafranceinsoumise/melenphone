from django.conf import settings
import requests
from requests.auth import AuthBase
from django.core.exceptions import ImproperlyConfigured

from ..exceptions import CallerCreationError, CallerValidationError

WEBHOOKS_ENDPOINT = 'https://api.callhub.io/v1/webhooks/'
AGENTS_ENDPOINT = 'https://api.callhub.io/v1/agents/'
VERIFY_AGENT_ENDPOINT = 'https://api.callhub.io/v2/agent-key/'


class CallhubAuth(AuthBase):
    def __init__(self, token):
        self._token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Token {}'.format(self._token)
        return r


def create_agent(user, username):
    email = user.email

    callhubData = {'username': username, 'email': email}

    r = requests.post(
        AGENTS_ENDPOINT,
        data=callhubData,
        auth=CallhubAuth(settings.CALLHUB_API_KEY)
    )

    if r.status_code == requests.codes.created:
        return
    elif r.status_code == 400:  # Bad request : le username existe déjà !
        raise CallerCreationError(detail="Ce nom d'agent est déjà utilisé sur Callhub")
    else:  # Autre erreur de callhub
        raise CallerCreationError


def verify_agent(username, password):
    callhubData = {"username": username, "password": password}

    r = requests.post(VERIFY_AGENT_ENDPOINT, data=callhubData)

    if r.status_code == requests.codes.ok:
        return
    elif r.status_code == 400:
        raise CallerValidationError(detail="L'identifiant et le mot de passe ne correspondent pas")
    else:
        raise CallerValidationError


def verify_wehbook():
    if settings.CALLHUB_WEBHOOK_DOMAIN is None:
        raise ImproperlyConfigured('Missing CALLHUB_WEBHOOK_DOMAIN setting')

    target = '{}/webhook/note'.format(settings.CALLHUB_WEBHOOK_DOMAIN)
    event = 'cc.notes'

    r = requests.get(WEBHOOKS_ENDPOINT, auth=CallhubAuth(settings.CALLHUB_API_KEY))
    r.raise_for_status()

    body = r.json()

    if 'results' not in body:
        raise ValueError('No results key in body')

    results = body['results']

    for webhook in results:
        if 'target' not in webhook and 'event' not in webhook:
            continue

        if webhook['target'] == target and webhook['event']:
            return True

    return False


def create_webhook():
    if settings.CALLHUB_WEBHOOK_DOMAIN is None:
        raise ImproperlyConfigured('Missing CALLHUB_WEBHOOK_DOMAIN setting')

    target = '{}/webhook/note'.format(settings.CALLHUB_WEBHOOK_DOMAIN)
    event = 'cc.notes'

    data = {
        'target': target,
        'event': event,
    }

    r = requests.post(
        WEBHOOKS_ENDPOINT,
        data=data,
        auth=CallhubAuth(settings.CALLHUB_API_KEY)
    )

    r.raise_for_status()
