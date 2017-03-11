# -*- coding: utf-8 -*-

#Django imports
from django.utils.http import urlquote_plus

#Project import
from callcenter.models import *

#Python imports
import numpy as np
import json
from random import randint
import requests
import phonenumbers

def setupLocationUser(user):
    city = user.city
    country_code = user.country_code
    userExtend = user.UserExtend

    # pour les belges
    if country_code == 'BE':
        location_lat = "51.229353"
        location_long = "4.401428"
    # pour les suisses
    elif country_code == 'CH':
        location_lat = "47.208101"
        location_long = "8.968452"
    # pour le reste du monde
    elif city and country_code:
        url = "https://nominatim.openstreetmap.org/search?format=json&city={city}&country_codes={country_code}".format(
            city=urlquote_plus(city),
            country_code=urlquote_plus(country_code)
        )

        res = requests.get(url) #On fait la requete sur l'API de geocoding

        if res.status_code == 200: #Si on a une réponse OK
            geocoding_data = res.json()

            if geocoding_data: # Si on a au moins 1 résultat
                location_lat = geocoding_data[0]['lat']
                location_long = geocoding_data[0]['lon']
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
    try:
        caller = UserExtend.objects.get(agentUsername=username) #Si l'appeleur est dans la bdd
        if caller.location_lat is None: #Si le mec n'a jamais appellé et qu'on ne connait pas sa pos
            setupLocationUser(caller.user)
        if caller.location_lat != "None": #Si on connait sa pos
            callerLat = caller.location_lat
            callerLng = caller.location_long
        else: #Si on connait pas la pos
            callerLat, callerLng = randomLocation() #On random
    except UserExtend.DoesNotExist: #Si on connait pas le user
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
