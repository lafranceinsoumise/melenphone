from django.conf import settings
import requests

from ..exceptions import CallerCreationError

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
        raise CallerCreationError(detail='username already used on callhub')
    else:  # Autre erreur de callhub
        raise CallerCreationError
