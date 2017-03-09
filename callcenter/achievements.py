# -*- coding: utf-8 -*-

#Django imports
from django.utils import timezone
#Project import
from callcenter.models import *

#Python imports
import datetime

#Fonction principale
def updateAchievements(user):
    calls = Appel.objects.filter(user=user).order_by('-date')
    
    #Appeler les autres fonctions de validation
    functions = [   leet,
                    callCount,
                    dailyCalls,
                    earlyAdopters
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

def earlyAdopters(user, calls):
    callersCount = calls.values('user').distinct().count()
    if callersCount < 100:
        unlockAchievement("early_y_etais", user)

def dailyCalls(user, calls):
    dailyCalls = calls.filter(date__gte=timezone.now() - datetime.timedelta(days=1)).count()
    if dailyCalls == 30:
        unlockAchievement("daily_a_fond", user)
    if dailyCalls == 50:
        unlockAchievement("daily_acharne", user)
    if dailyCalls == 100:
        unlockAchievement("daily_dodo", user)


def callCount(user, calls):
    count = calls.count()
    if count == 1:
        unlockAchievement("count_insoumis_1", user)
    if count == 5:
        unlockAchievement("count_insoumis_2", user)
    if count == 10:
        unlockAchievement("count_insoumis_3", user)
    if count == 20:
        unlockAchievement("count_insoumis_4", user)
    if count == 35:
        unlockAchievement("count_insoumis_5", user)
    if count == 50:
        unlockAchievement("count_membre_appui", user)
    if count == 70:
        unlockAchievement("count_createur_appui", user)
    if count == 100:
        unlockAchievement("count_conseiller_suppleant", user)
    if count == 150:
        unlockAchievement("count_conseiller_titulaire", user)
    if count == 250:
        unlockAchievement("count_adjoint", user)
    if count == 375:
        unlockAchievement("count_maire", user)
    if count == 500:
        unlockAchievement("count_directeur", user)
    if count == 700:
        unlockAchievement("count_conseiller_departemental", user)
    if count == 1000:
        unlockAchievement("count_president_departemental", user)
    if count == 1500:
        unlockAchievement("count_conseiller_regional", user)
    if count == 2000:
        unlockAchievement("count_president_regional", user)
    if count == 2750:
        unlockAchievement("count_depute_5", user)
    if count == 3750:
        unlockAchievement("count_depute_constituante", user)
    if count == 5000:
        unlockAchievement("count_depute_6", user)
