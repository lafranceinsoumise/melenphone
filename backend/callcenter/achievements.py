# -*- coding: utf-8 -*-

#Python imports
import redis
import json

#Django imports
from django.utils import timezone

#Project import
from callcenter.models import *
from melenchonPB.redis import redis_pool, format_date
from callcenter.consumers import send_message

#Fonction principale
def updateAchievements(user):
    if not(user is None):
        #Appeler les autres fonctions de validation
        functions = [   leet,
                        callCount,
                        dailyCalls,
                        earlyAdopters,
                        leaderboards
                    ]
        for f in functions:
            f(user)

def unlockAchievement(codeName, user):
    try:
        achievement = Achievement.objects.get(codeName=codeName)
    except Achievement.DoesNotExist:
        pass
    achievementUnlock, created = AchievementUnlock.objects.get_or_create(userExtend=user.UserExtend, achievement=achievement)
    if created: #Si l'achievement est débloqué, on crédite les phis associés
        userExtend = user.UserExtend
        userExtend.phi = userExtend.phi + (achievement.phi * userExtend.phi_multiplier)
        userExtend.save()

        #Pas de websocket si l'achievement est trop banal.
        excluded_achievements = [
            'count_initie',
            'count_apprenti'
        ]

        if codeName not in excluded_achievements:
            websocketMessage = json.dumps({'type': 'achievement',
                                       'value': {
                                            'agentUsername':userExtend.agentUsername,
                                            'achievement':{
                                                'name':achievement.name,
                                                'condition':achievement.condition,
                                                'phi':achievement.phi,
                                                'codeName':achievement.codeName
                                            }
                                       }
                                    })
            send_message(websocketMessage)


########### ACHIEVEMENT CONDITIONS ################


def leet(user):
    now = timezone.now().astimezone(timezone.get_default_timezone())
    if(now.hour == 13 and now.minute == 37):
        unlockAchievement("leet", user)

def earlyAdopters(user):
    r = redis.StrictRedis(connection_pool=redis_pool)
    callersCount = r.scard('leaderbords:alltime')
    if callersCount < 100:
        unlockAchievement("early_y_etais", user)

def dailyCalls(user):
    r = redis.StrictRedis(connection_pool=redis_pool)
    dailyCalls = int(r.zscore('melenphone:leaderboards:daily:' + format_date(timezone.now()), str(user.id)))
    if dailyCalls == 50:
        unlockAchievement("daily_a_fond", user)
    if dailyCalls == 100:
        unlockAchievement("daily_acharne", user)
    if dailyCalls == 200:
        unlockAchievement("daily_dodo", user)


def callCount(user):
    r = redis.StrictRedis(connection_pool=redis_pool)
    count = int(r.zscore('melenphone:leaderboards:alltime', str(user.id)))
    if count == 1:
        unlockAchievement("count_initie", user)
    if count == 5:
        unlockAchievement("count_apprenti", user)
    if count == 10:
        unlockAchievement("count_fan_rdls", user)
    if count == 20:
        unlockAchievement("count_militant", user)
    if count == 35:
        unlockAchievement("count_top", user)
    if count == 50:
        unlockAchievement("count_messager", user)
    if count == 70:
        unlockAchievement("count_animateur", user)
    if count == 100:
        unlockAchievement("count_artiste", user)
    if count == 150:
        unlockAchievement("count_lanceur", user)
    if count == 250:
        unlockAchievement("count_ambassadeur", user)
    if count == 375:
        unlockAchievement("count_mage", user)
    if count == 500:
        unlockAchievement("count_justicier", user)
    if count == 700:
        unlockAchievement("count_tribun", user)
    if count == 1000:
        unlockAchievement("count_heros", user)
    if count == 1500:
        unlockAchievement("count_laec", user)
    if count == 5000:
        unlockAchievement("count_legendaire", user)

def leaderboards(user):
    r = redis.StrictRedis(connection_pool=redis_pool)

    if int(r.zrevrank('melenphone:leaderboards:alltime', str(user.id))) == 0:
        unlockAchievement("leaderboard_alltime", user)

    if int(r.zrevrank('melenphone:leaderboards:weekly:' + format_date(timezone.now()), str(user.id))) == 0:
        unlockAchievement("leaderboard_weekly", user)

    if int(r.zrevrank('melenphone:leaderboards:daily:' + format_date(timezone.now()), str(user.id))) == 0:
        unlockAchievement("leaderboard_daily", user)