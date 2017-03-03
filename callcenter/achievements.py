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
        calls = Appel.objects.filter(user=user).order_by('-date')
        #Appeler les autres fonctions de validation
        functions = [   leet,
                        callCount
                    ]
        for f in functions:
            f(user, calls)

def unlockAchievement(codeName, user):
    if Achievement.objects.filter(codeName=codeName).exists():
        achievement = Achievement.objects.filter(codeName=codeName)[0]
        achievementUnlock, created = AchievementUnlock.objects.get_or_create(userExtend=user.UserExtend, achievement=achievement)
        if created: #Si l'achievement est débloqué, on crédite les phis associés
            userExtend = user.UserExtend
            userExtend.phi = userExtend.phi + (achievement.phi * userExtend.phi_multiplier)
            userExtend.save()


########### ACHIEVEMENT CONDITIONS ################


def leet(user, calls):
    lastCall = calls[0].date
    if lastCall.minute == 37 and lastCall.hour == 13:
        unlockAchievement("leet", user)

def callCount(user, calls):
    count = calls.count
    if count = 1:
        unlockAchievement("count_insoumis", user)
    if count = 10:
        unlockAchievement("count_insoumis_qualite", user)
    if count = 50:
        unlockAchievement("count_conseiller_issou", user)
