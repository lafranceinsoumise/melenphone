# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.db import models
from callcenter.models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import requests
from django.conf import settings
import json
from .forms import *

def index(request):
    return render(request, 'callcenter/index.html', locals())

def registerNew(request):
    if request.method == 'POST':
        form = registerNewForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            ville=form.cleaned_data['ville']
            headers = {'Authorization': 'Token %s' % settings.API_KEY}
            data = {'username':username, 'email':email, 'team':'tout_le_monde'}
            r = requests.post('https://api.callhub.io/v1/agents/', data=data, headers=headers)
            if r.status_code == requests.codes.created: #Tout s'est bien passé
                user,created = User.objects.get_or_create(username=username, email=email)
                if created:
                    user.set_password(password)
                    user.save()
                    userExtend, created = UserExtend.objects.get_or_create(ville=ville, agentUsername=username, phi=0, user=user)
                    if created:
                        userExtend.save()
                        return redirect('register_sucess')
                    else:
                        user.delete()
                        form.add_error(None, "Une erreur est survenue.")
                else:
                    form.add_error(None, "Une erreur est survenue.")
            elif r.status_code == 400: #Bad request : le username existe déjà !
                form.add_error('username', "Ce nom d'utilisateur est déjà utilisé sur Callhub !")
            else: #Autre erreur de callhub
                form.add_error(None, "Callhub ne répond pas, veuillez réessayer plus tard.")
    else:
        form=registerNewForm()
    return render(request, 'callcenter/register.html', locals())

def registerSucess(request):
    return render(request, 'callcenter/register_success.html', locals())


#View pour faire les tests
def test(request):
    url = 'https://api.callhub.io/v1/agents/'
    headers = {'Authorization': 'Token %s' % settings.API_KEY}
    agents = requests.get(url, headers=headers)
    #On verifie que le username n'existe pas deja
    test = json.loads(agents.text)['results'][0]
    return render(request, 'callcenter/test.html', locals())

""" TESTS API
def agent_key(request):
    data = {"username":"DarckouneAgentTest", "password":"jambon75"}
    key = requests.post('https://api.callhub.io/v2/agent-key/', data=data)
    print "Agent Key", key.json()
    return render(request, 'callcenter/test.html', locals())

def agent_status(request):
    key = "Token d97812bc859466a7b9826c67e944c3ca96fd4aa6"
    url = "https://api.callhub.io/v2/agent-status/"
    headers = {"Authorization": key}
    r = requests.get(url, headers=headers)
    print r.text
    return render(request, 'callcenter/agent_status.html', locals())

def set_webhook(request):
    key = 'Token ' # API KEY
    url = "https://api.callhub.io/v1/webhooks/"
    headers = {"Authorization": key}
    data = {'event':'cc.notes', 'target':'http://requestb.in/1bas5go1'}
    r = requests.post(url, data=data, headers=headers)
    return render(request, 'callcenter/test.html', locals())

def get_webhook(request):
    key = 'Token ' #API KEY
    headers = {'Authorization': key}
    url = 'https://api.callhub.io/v1/webhooks/'
    r = requests.get(url, headers=headers)
    return render(request, 'callcenter/webhooks.html', locals())

def campaign_info(request):
    key = 'Token d97812bc859466a7b9826c67e944c3ca96fd4aa6'
    headers = {'Authorization': key}
    url = 'https://api.callhub.io/v2/campaign-info/?id=[5335]'
    r = requests.get(url, headers=headers)
    return render(request, 'callcenter/campaign_info.html', locals())

def is_trophy(request):
    campaign = "5338"
    key = 'Token d97812bc859466a7b9826c67e944c3ca96fd4aa6'
    headers = {'Authorization': key}
    url = 'https://api.callhub.io/v2/is-trophy/' + campaign + '/'
    r = requests.get(url, headers=headers)
    return render(request, 'callcenter/is_trophy.html', locals())
"""
