# -*- coding: utf-8 -*-

#Django imports
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils import timezone

#Python imports
import datetime

#Project import
from callcenter.models import Appel, UserExtend
from callcenter.achievements import unlockAchievement

class Command(BaseCommand):
    def handle(self, *args, **options):

        #On reset les placements
        UserExtend.objects.all().update(daily_leaderboard=0, weekly_leaderboard=0, alltime_leaderboard=0)

        #Mise à jour du alltime_leaderboard
        leaders = Appel.objects.values('user').annotate(Count('user')).order_by('-user__count')

        for index, leader in enumerate(leaders):
            userID = leader['user']
            calls = leader['user__count']
            userExtend = User.objects.filter(id=userID)[0].UserExtend
            userExtend.alltime_leaderboard = index + 1
            userExtend.alltime_leaderboard_calls = calls
            userExtend.save()

        #On débloque le succes "Avoir été n°1 du classement" au premier de la liste
        leader = User.objects.filter(id=leaders[0]['user'])[0]
        unlockAchievement("leaderboard_alltime", leader)

        #Mise à jour du weekly_leaderboard
        leaders = Appel.objects.filter(date__gte=timezone.now() - datetime.timedelta(days=7)).values('user').annotate(Count('user')).order_by('-user__count')

        for index, leader in enumerate(leaders):
            userID = leader['user']
            calls = leader['user__count']
            userExtend = User.objects.filter(id=userID)[0].UserExtend
            userExtend.weekly_leaderboard = index + 1
            userExtend.weekly_leaderboard_calls = calls
            userExtend.save()

        #On débloque le succes "Avoir été n°1 du classement hebdo" au premier de la liste
        leader = User.objects.filter(id=leaders[0]['user'])[0]
        unlockAchievement("leaderboard_weekly", leader)

        #Mise à jour du daily_leaderboard
        leaders = Appel.objects.filter(date__gte=timezone.now() - datetime.timedelta(days=1)).values('user').annotate(Count('user')).order_by('-user__count')

        for index, leader in enumerate(leaders):
            userID = leader['user']
            calls = leader['user__count']
            userExtend = User.objects.filter(id=userID)[0].UserExtend
            userExtend.daily_leaderboard = index + 1
            userExtend.daily_leaderboard_calls = calls
            userExtend.save()

        #On débloque le succes "Avoir été n°1 du classement du jour" au premier de la liste
        leader = User.objects.filter(id=leaders[0]['user'])[0]
        unlockAchievement("leaderboard_daily", leader)
