# -*- coding: utf-8 -*-

# Python imports
import redis
import datetime

# Django imports
from django.utils import timezone
from channels import Channel

# Project import
from callcenter.models import *
from melenchonPB.redis import get_redis_instance, format_date


# Fonction principale
def update_achievements(user):
    if not (user is None):
        # Appeler les autres fonctions de validation
        functions = [
            leet,
            callCount,
            dailyCalls,
            leaderboards,
            consecutive
        ]
        for f in functions:
            f(user)


def unlock_achievement(codeName, user):
    try:
        achievement = Achievement.objects.get(codeName=codeName)
    except Achievement.DoesNotExist:
        pass
    achievementUnlock, created = AchievementUnlock.objects.get_or_create(userExtend=user.UserExtend,
                                                                         achievement=achievement)
    if created:  # Si l'achievement est débloqué, on crédite les phis associés
        userExtend = user.UserExtend
        userExtend.phi = userExtend.phi + (achievement.phi * userExtend.phi_multiplier)
        userExtend.save()

        message = {
            'type': 'achievement',
            'value': {
                'agentUsername': userExtend.agentUsername,
                'achievement': {
                    'name': achievement.name,
                    'condition': achievement.condition,
                    'phi': achievement.phi,
                    'codeName': achievement.codeName
                }
            }
        }
        Channel('send_message').send(message)


def get_achievements(user):
    try:
        unlocked_achievements = user.UserExtend.get_achievements()
    except UserExtend.DoesNotExist:
        unlocked_achievements = []

    data = {}

    # Recuperation des achivements débloqués
    data_unlocked_achievements = []
    id_list = []
    for achievement in unlocked_achievements:
        data_unlocked_achievements.append({
            'name': achievement.name,
            'condition': achievement.condition,
            'phi': achievement.phi,
            'codeName': achievement.codeName
        })
        id_list.append(achievement.id)

    # Recuperation des achivements restants
    locked_achievements = Achievement.objects.all().exclude(id__in=id_list)

    data_locked_achievements = []
    for achievement in locked_achievements:
        data_locked_achievements.append(
            {'name': achievement.name, 'condition': achievement.condition, 'phi': achievement.phi})

    data['unlocked'] = data_unlocked_achievements[::-1]
    data['locked'] = data_locked_achievements

    return data


########### ACHIEVEMENT CONDITIONS ################


def leet(user):
    now = timezone.now().astimezone(timezone.get_default_timezone())
    if (now.hour == 13 and now.minute == 37):
        unlock_achievement("leet", user)


def earlyAdopters(user):
    r = get_redis_instance()
    callersCount = r.scard('melenphone:leaderbords:alltime')
    if callersCount < 100:
        unlock_achievement("early_y_etais", user)


def dailyCalls(user):
    r = get_redis_instance()
    dailyCalls = int(r.zscore('melenphone:leaderboards:daily:' + format_date(timezone.now()), str(user.id)))
    if dailyCalls == 50:
        unlock_achievement("daily_a_fond", user)
    if dailyCalls == 100:
        unlock_achievement("daily_acharne", user)
    if dailyCalls == 200:
        unlock_achievement("daily_dodo", user)
    if dailyCalls == 300:
        unlock_achievement("daily_holochon", user)


def callCount(user):
    r = get_redis_instance()
    count = int(r.zscore('melenphone:leaderboards:alltime', str(user.id)))
    if count == 1:
        unlock_achievement("count_initie", user)
    if count == 5:
        unlock_achievement("count_apprenti", user)
    if count == 10:
        unlock_achievement("count_fan_rdls", user)
    if count == 20:
        unlock_achievement("count_militant", user)
    if count == 35:
        unlock_achievement("count_top", user)
    if count == 50:
        unlock_achievement("count_messager", user)
    if count == 70:
        unlock_achievement("count_animateur", user)
    if count == 100:
        unlock_achievement("count_artiste", user)
    if count == 150:
        unlock_achievement("count_lanceur", user)
    if count == 250:
        unlock_achievement("count_ambassadeur", user)
    if count == 375:
        unlock_achievement("count_mage", user)
    if count == 500:
        unlock_achievement("count_justicier", user)
    if count == 700:
        unlock_achievement("count_tribun", user)
    if count == 1000:
        unlock_achievement("count_heros", user)
    if count == 1500:
        unlock_achievement("count_laec", user)
    if count == 5000:
        unlock_achievement("count_legendaire", user)


def leaderboards(user):
    r = get_redis_instance()

    if int(r.zrevrank('melenphone:leaderboards:alltime', str(user.id))) == 0:
        unlock_achievement("leaderboard_alltime", user)

    if int(r.zrevrank('melenphone:leaderboards:weekly:' + format_date(timezone.now()), str(user.id))) == 0:
        unlock_achievement("leaderboard_weekly", user)

    if int(r.zrevrank('melenphone:leaderboards:daily:' + format_date(timezone.now()), str(user.id))) == 0:
        unlock_achievement("leaderboard_daily", user)

def consecutive(user):
    r = get_redis_instance()
    time = timezone.now()
    days = 0

    while r.zscore('melenphone:leaderboards:daily:' + format_date(time), str(user.id)) != None:
        days += 1
        if days == 2:
            unlock_achievement("consecutive_retour", user)
        elif days == 3:
            unlock_achievement("consecutive_fidele", user)
        elif days == 5:
            unlock_achievement("consecutive_infatigable", user)
        elif days == 10:
            unlock_achievement("consecutive_melenphonophile", user)
        time -= datetime.timedelta(days=1)
