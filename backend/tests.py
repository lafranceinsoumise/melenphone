from accounts.models import User
from callcenter.models import UserExtend
from callcenter.actions.score import update_scores
import requests
import time
from django.db import IntegrityError
import random

def create_member(username):
    try:
        user = User.objects.create(email = username + "@gmail.com")
        UserExtend.objects.create(user=user, agentUsername=username)
        update_scores(user)
    except IntegrityError as e:
        print("Ca marche pas :(")

def create_mass_member(number):
    users = []
    userextends = []
    for i in range (number):
        user = User(id=i, email = str(i) + "@gmail.com")
        userextend = UserExtend(user_id=i, agentUsername=str(i))
        users.append(user)
        userextends.append(userextend)
    User.objects.bulk_create(users)
    UserExtend.objects.bulk_create(userextends)
    for user in users:
        update_scores(user)


def mass_call(nombre):
    for i in range (nombre):
        temps = random.randint(0,2000)/1000
        requests.post('http://localhost:8000/api/simulate_call')
        time.sleep(temps)

def mass_call_fast(nombre):
    for i in range (nombre):
        requests.post('http://localhost:8000/api/simulate_call')