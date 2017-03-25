from django.conf import settings
import requests

from ..exceptions import CallerCreationError, CallerValidationError

def create_agent(user, username):
    email = user.email

    token = 'Token ' + settings.CALLHUB_API_KEY
    headers = {'Authorization': token}
    callhubData = {'username': username, 'email': email}

    r = requests.post('https://api.callhub.io/v1/agents/', data=callhubData,
                      headers=headers)

    if r.status_code == requests.codes.created:
        return
    elif r.status_code == 400:  # Bad request : le username existe déjà !
        raise CallerCreationError(detail="Ce nom d'agent est déjà utilisé sur Callhub")
    else:  # Autre erreur de callhub
        raise CallerCreationError

def verify_agent(username, password):

    callhubData = {"username": username, "password": password}

    r = requests.post('https://api.callhub.io/v2/agent-key/', data=callhubData)

    if r.status_code == requests.codes.ok:
        return
    elif r.status_code == 400:
        raise CallerValidationError(detail="username and password doesn't match")
    else:
        raise CallerValidationError