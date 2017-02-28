# -*- coding: utf-8 -*-

#Django imports
from django.conf import settings

#Project import
from callcenter.models import *

#Python imports
import numpy as np
import json
from random import randint
import requests
import phonenumbers

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

#Parcourt le tableau AreaData pour chercher un cas où latmin < lat < latmax et lngmin < lng < lngmax
def findCaseSVG(AreaData, lat, lng):
    for i in range (len(AreaData)):
        if ((AreaData[i][0] > lat) and (AreaData[i][1] < lat) and (AreaData[i][2] < lng) and (AreaData[i][3]) > lng):
            return (i)
    return (len(AreaData))

def setupLocationUser(user):
    userExtend = user.UserExtend
    address = userExtend.address
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ address + '&key=' + settings.GOOGLE_MAPS_API_KHEY
    googleAPIRequest = requests.get(url) #On fait la requete sur l'API de Google maps
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
    userExtend.location_lat = location_lat
    userExtend.location_long = location_long
    userExtend.save()

def randomLocation():
    count = NumbersLocation.objects.all().count()
    randomIndex = randint(0,count-1)
    randomPlace = NumbersLocation.objects.all()[randomIndex]
    return randomPlace.location_lat, randomPlace.location_long

def getCallerLocation(username):
    if UserExtend.objects.filter(agentUsername=username).exists(): #Si l'appeleur est dans la bdd
        caller = UserExtend.objects.filter(agentUsername=username)[0].user
        if caller.UserExtend.location_lat is None: #Si le mec n'a jamais appellé et qu'on ne connait pas sa pos
            setupLocationUser(caller)
        if caller.UserExtend.location_lat != "None": #Si on connait sa pos
            callerLat = caller.UserExtend.location_lat
            callerLng = caller.UserExtend.location_long
        else: #Si on connait pas la pos
            callerLat, callerLng = randomLocation() #On random
    else: #Si on connait pas le user
        callerLat, callerLng = randomLocation() #On random
    return callerLat, callerLng

def getCalledLocation(number):
    countryCode = phonenumbers.parse("+" + number, None).country_code
    if countryCode == 33: #Si on est en france, on cherche plus précisement
        if NumbersLocation.objects.filter(pays="33", zone=number[2:3], indicatif=number[3:5]).exists():
            calledPlace = NumbersLocation.objects.filter(pays=33, zone=number[2:3], indicatif=number[3:5])[0]
            calledLat = calledPlace.location_lat
            calledLng = calledPlace.location_long
        else:
            calledLat, calledLng = randomLocation()
    else:
        if NumbersLocation.objects.filter(pays=str(countryCode)).exists():
            calledPlace = NumbersLocation.objects.filter(pays=str(countryCode))[0]
            calledLat = calledPlace.location_lat
            calledLng = calledPlace.location_long
        else:
            calledLat, calledLng = randomLocation()
    return calledLat, calledLng
