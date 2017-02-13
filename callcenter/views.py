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
import numpy as np

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
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=Paris+France&key=' + settings.GOOGLE_MAPS_API_KHEY
    r = requests.get(url)
    googleAPIRequest = requests.get(url)
    googleAPIData = json.loads(googleAPIRequest.text)
    location_lat = (googleAPIData['results'][0]['geometry']['location']['lat'])
    location_long = (googleAPIData['results'][0]['geometry']['location']['lng'])
    (X,Y) = getSVGPos(location_lat, location_long)
    test = "X : " + str(X) + " Y : " + str(Y)
    return render(request, 'callcenter/test.html', locals())


def getSVGPos(lat,lng):
    #Latitude : X (augmente vers le nord)
    #Longitude : Y (augmente vers l'est)
    # Format sous tableaux : [lat_nord / Ymin, lat_sud / Ymax ,lng_ouest / Xmin ,lng_est / Xmax ]

    SVGData = [[0.001123,0.701235,0.177445,0.687332], #Region 0 FRANCE METROPOLITAINE
                    ]
    AreaData = [[51.088954,42.333188,-4.796524,8.203037], #Region 0 FRANCE METROPOLITAINE
                    ]

    region = findCaseSVG(AreaData, lat, lng) # On cherche dans quelle region on est

    #Calcul de la position sur le SVG :

    #Transformation en radians de la lat :
    AreaData[region][0] = AreaData[region][0]*np.pi/180
    AreaData[region][1] = AreaData[region][1]*np.pi/180
    lat = lat*np.pi/180
    
    #Projection de mercator
    AreaData[region][0] = np.log(np.tan(AreaData[region][0]) + (1/np.cos(AreaData[region][0])))
    AreaData[region][1] = np.log(np.tan(AreaData[region][1]) + (1/np.cos(AreaData[region][1])))
    lat = np.log(np.tan(lat) + (1/np.cos(lat)))

    # Y = Ymin + ((lat_nord - lat)/(lat_nord - lat_sud))*(Ymax-Ymin)
    YSVG = SVGData[region][0] + (((AreaData[region][0] - lat) / (AreaData[region][0] - AreaData[region][1])) * (SVGData[region][1] - SVGData[region][0]))

    # X = Xmin + ((lng - lng_ouest)/(lng_est - lng_ouest))*(Xmax-Xmin)
    XSVG = SVGData[region][2] + (((lng - AreaData[region][2]) / (AreaData[region][3] - AreaData[region][2])) * (SVGData[region][3] - SVGData[region][2]))

    return(XSVG, YSVG)

def findCaseSVG(AreaData, lat, lng):

    for i in range (len(AreaData)):
        if ((AreaData[i][0] > lat) and (AreaData[i][1] < lat) and (AreaData[i][2] < lng) and (AreaData[i][3]) > lng):
            return (i)

    return (len(AreaData))
