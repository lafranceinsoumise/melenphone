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
            print (location_lat)
            print (location_long)
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
