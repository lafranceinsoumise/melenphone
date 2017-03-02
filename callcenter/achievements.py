# -*- coding: utf-8 -*-

#Django imports

#Project import
from callcenter.models import *

#Python imports
import datetime

#Fonction principale
def updateAchievements(agentUsername):
    if UserExtend.objects.filter(agentUsername=agentUsername).exists(): #On check si le user existe
        user = UserExtend.objects.filter(agentUsername=agentUsername)[0].user
        #Appeler les autres fonctions
        functions = [leet]
        for f in functions:
            f(user)

def leet(user):
    lastCall = Appel.objects.filter(user=user).order_by('-date')[0].date
    if date.minute == 37 and date.hour == 13:
        pass #Unlock l'achievement leet
