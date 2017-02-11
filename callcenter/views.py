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
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def noteWebhook(request):
    jsondata = request.body
    data = json.loads(jsondata)

    #Verifier la date du dernier appel (au moins 1mn entre chaque appel ?)
        #Ajouter une entrée dans la table Appel
        #Verifier les achievements

    return HttpResponse(status=200)

def index(request):
    return render(request, 'callcenter/index.html', locals())

def registerNew(request):
    if request.method == 'POST':
        form = registerNewForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            country=form.cleaned_data['country']
            city=form.cleaned_data['city']
            token = 'Token ' + settings.CALLHUB_API_KHEY
            headers = {'Authorization': token }
            data = {'username':username, 'email':email, 'team':'tout_le_monde'}
            r = requests.post('https://api.callhub.io/v1/agents/', data=data, headers=headers)
            if r.status_code == requests.codes.created: #Tout s'est bien passé

                #On recup la localisation via l'API Google maps.
                adress = city + '+' + country
                adress.replace(" ", "+")
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ adress + '&key=' + settings.GOOGLE_MAPS_API_KHEY
                googleAPIRequest = requests.get(url)
                if googleAPIRequest.status_code == 200: #Si on a une réponse de google
                    googleAPIData = json.loads(googleAPIRequest.text)
                    if googleAPIData['status'] == "OK": #Si google a un resultat, on le récupere
                        location_lat = str(googleAPIData['results'][0]['geometry']['location']['lat'])
                        location_long = str(googleAPIData['results'][0]['geometry']['location']['lng'])
                        print location_lat
                        print location_long
                    else: #Si google n'a pas de résultats, on ne connait pas la localisation
                        location_lat="None"
                        location_long="None"
                else: #Si on a pas une réponse de google, on ne connait pas la localisation
                    location_lat="None"
                    location_long="None"
                #On crée le user dans la bdd
                user,created = User.objects.get_or_create(username=username, email=email)
                if created:
                    user.set_password(password)
                    user.save()
                    userExtend, created = UserExtend.objects.get_or_create(agentUsername=username, phi=0, location_lat=location_lat, location_long=location_long, user=user)
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
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=york+US&key=' + settings.GOOGLE_MAPS_API_KHEY
    r = requests.get(url)
    return render(request, 'callcenter/test.html', locals())
