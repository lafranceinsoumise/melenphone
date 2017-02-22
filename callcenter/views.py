# -*- coding: utf-8 -*-

#Django imports
from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View, TemplateView

#Python imports
import requests
import json

#Project imports
from callcenter.models import *
from callcenter.map import *
from .forms import *


class AngularApp(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(AngularApp, self).get_context_data(**kwargs)
        context['ANGULAR_URL'] = settings.ANGULAR_URL
        return context

class SampleView(View):
    """View to render django template to angular"""
    def get(self, request):
        return render("OK!")

class NgTemplateView(View):
    """View to render django template to angular"""
    def get(self, request):
        return render(request, 'template.html', {"django_variable": "This is django context variable"})

@require_POST
@csrf_exempt #Sinon la requete est bloquée car lancée depuis un autre site (donc qui n'a pas le cookie csrf)
def noteWebhook(request):
    jsondata = request.body
    data = json.loads(jsondata)

    #Latitude et longitude de l'appelant
    callerAgentUsername = data['data']['agent']['username']
    if User.objects.filter(username=callerAgentUsername).exists(): #Si l'appeleur est dans la bdd
        caller = User.objects.filter(username=callerAgentUsername)[0]

        if caller.UserExtend.location_lat is None: #Si le mec n'a jamais appellé et qu'on ne connait pas sa pos
            setupLocationUser(caller)

        if caller.UserExtend.location_lat != "None": #Si on connait sa pos
            callerLat = caller.UserExtend.location_lat
            callerLng = caller.UserExtend.location_long
        else: #Si on connait pas la pos
            callerLat, callerLng = randomLocation() #On random
    else: #Si on connait pas le user
        callerLat, callerLng = randomLocation() #On random

    #Latitude et longitude de l'appellé
    calledNumber = data['data']['contact']
    firstNumbers = calledNumber[:5]
    if NumbersLocation.objects.filter(code=firstNumbers).exists():
        calledPlace = NumbersLocation.objects.filter(code=firstNumbers)[0]
        calledLat = calledPlace.location_lat
        calledLng = calledPlace.location_long
    else:
        calledLat, calledLng = randomLocation()

    print ("Appelant : Lat : " + callerLat + " Lng : " + callerLng)
    print ("Cible : Lat : " + calledLat + " Lng : " + calledLng)
    return HttpResponse(status=200)

def index(request):
    return render(request, 'callcenter/index.html', locals())


# View pour l'enregistrement d'un nouveau membre et création de son agent callhub
def registerNew(request):
    if request.method == 'POST':
        form = registerNewForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            country=form.cleaned_data['country']
            city=form.cleaned_data['city']

            address = city + '+' + country
            address.replace(" ", "+")

            token = 'Token ' + settings.CALLHUB_API_KHEY
            headers = {'Authorization': token }
            data = {'username':username, 'email':email, 'team':'tout_le_monde'}
            r = requests.post('https://api.callhub.io/v1/agents/', data=data, headers=headers) #On fait la requete sur l'API de github
            if r.status_code == requests.codes.created: #Si tout s'est bien passé
                #On crée le user dans la bdd
                user,created = User.objects.get_or_create(username=username, email=email) #On tente de créer le user
                if created:
                    user.set_password(password)
                    user.save()
                    #On crée alors la partie userextend
                    userExtend, created = UserExtend.objects.get_or_create(agentUsername=username, phi=0, address=address, user=user)
                    if created:
                        userExtend.save()
                        return redirect('register_sucess')
                    else: #Si y'a un problème, on supprime le User créé juste avant
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

#View de transition après enregistrement d'un nouvel utilisateur
def registerSucess(request):
    return render(request, 'callcenter/register_success.html', locals())

#View pour faire les tests
def test(request):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=Paris+France&key=' + settings.GOOGLE_MAPS_API_KHEY
    r = requests.get(url)
    googleAPIRequest = requests.get(url)
    googleAPIData = json.loads(googleAPIRequest.text)
    location_lat = (googleAPIData['results'][0]['geometry']['location']['lat'])
    location_long = (googleAPIData['results'][0]['geometry']['location']['lng'])
    (X,Y) = getSVGPos(location_lat, location_long)
    test = "X : " + str(X) + " Y : " + str(Y)
    return render(request, 'callcenter/test.html', locals())
