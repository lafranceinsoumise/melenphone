# -*- coding: utf-8 -*-

import json
import random

import redis
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView

from accounts.models import User
from callcenter.actions.leaderboard import generate_leaderboards
from callcenter.actions.map import getCallerLocation, getCalledLocation, randomLocation
from callcenter.actions.phi import EarnPhi
from callcenter.consumers import send_message
from callcenter.exceptions import CallerCreationError, CallerValidationError
from callcenter.models import *
from callcenter.serializers import UserSerializer, UserExtendSerializer, CallhubCredentialsSerializer
from melenchonPB.redis import redis_pool, format_date


#################### WEBHOOKS ################################


# /webhook/note
class webhook_note(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):

        jsondata = request.body.decode('utf-8')
        data = json.loads(jsondata)

        #Latitude et longitude de l'appelant
        callerAgentUsername = data['data']['agent']['username']
        callerLat, callerLng = getCallerLocation(callerAgentUsername)

        #Latitude et longitude de l'appellé
        calledNumber = data['data']['contact']
        calledLat, calledLng = getCalledLocation(calledNumber)

        r = redis.StrictRedis(connection_pool=redis_pool)

        now = timezone.now().timestamp()

        try:
            user = UserExtend.objects.get(agentUsername=callerAgentUsername).user #On le récupère
            lastCall = float(r.getset('lastcall:user:' + str(user.id), now) or 0)
        except UserExtend.DoesNotExist:
            user = None
            lastCall = None

        if lastCall is None or (now - lastCall > settings.MIN_DELAY):
            #On crédite les phis que gagne le user
            EarnPhi(user, lastCall)
            Call.objects.create(user=user)

            #On envoie les positions au websocket pour l'animation
            if user is None:
                id = None
                agentUsername = None
            else:
                id = user.id
                agentUsername = user.UserExtend.agentUsername

            dailyCalls = int(r.get('melenphone:call_count:daily:' + format_date(timezone.now())) or 0)
            weeklyCalls = int(r.get('melenphone:call_count:weekly:' + format_date(timezone.now())) or 0)
            alltimeCalls = int(r.get('melenphone:call_count:alltime') or 0)

            ranking = r.zrevrange('melenphone:leaderboards:daily:' + format_date(timezone.now()), 0, 9, withscores=True)
            dailyLeaderboard = []
            for ranked in ranking:
                try:
                    username = User.objects.get(id=int(ranked[0])).UserExtend.agentUsername
                except User.DoesNotExist:
                    username = "Unknown"
                calls = int(ranked[1])
                dailyLeaderboard.append({'username': username, 'calls': calls})

            websocketMessage = json.dumps({ 'type':'call',
                                            'value':{
                                                 'call': {
                                                    'caller': {
                                                        'lat':callerLat,
                                                        'lng':callerLng,
                                                        'id':id,
                                                        'agentUsername':agentUsername},
                                                    'target': {
                                                        'lat':calledLat,
                                                        'lng':calledLng}
                                                    },
                                                'updatedData': {
                                                    'dailyCalls':dailyCalls,
                                                    'weeklyCalls':weeklyCalls,
                                                    'alltimeCalls':alltimeCalls,
                                                    'dailyLeaderboard': dailyLeaderboard
                                                    }
                                            }
                                        })
            send_message(websocketMessage)

        return HttpResponse(status=200)


#################### REST API ################################

# /api/test_websocket/
class api_test_socket(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        if settings.DEBUG == False:
            raise Http404
        send_message(request.body)
        return HttpResponse(200)


# /api/simulate_call/
class api_test_simulatecall(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        if settings.DEBUG == False:
            raise Http404

        r = redis.StrictRedis(connection_pool=redis_pool)

        users = User.objects.all()
        nb = users.count()
        user = users[random.randint(0, nb-1)]
        now = timezone.now().timestamp()

        callerLat, callerLng = randomLocation()
        calledLat, calledLng = randomLocation()

        lastCall = float(r.getset('lastcall:user:' + str(user.id), now) or 0)
        EarnPhi(user, lastCall)

        # On ajoute l'appel à la bdd pour pouvoir reconstruire redis si besoin
        Call.objects.create(user=user)

        dailyCalls = int(r.get('melenphone:call_count:daily:' + format_date(timezone.now())) or 0)
        weeklyCalls = int(r.get('melenphone:call_count:weekly:' + format_date(timezone.now())) or 0)
        alltimeCalls = int(r.get('melenphone:call_count:alltime') or 0)

        ranking = r.zrevrange('melenphone:leaderboards:daily:' + format_date(timezone.now()), 0, 9, withscores=True)
        dailyLeaderboard = []
        for ranked in ranking:
            username = User.objects.filter(id=int(ranked[0]))[0].UserExtend.agentUsername
            calls = int(ranked[1])
            dailyLeaderboard.append({'username': username, 'calls': calls})

        websocketMessage = json.dumps({'type': 'call',
                                       'value': {
                                           'call': {
                                               'caller': {
                                                   'lat': callerLat,
                                                   'lng': callerLng,
                                                   'id': user.id,
                                                   'agentUsername': user.UserExtend.agentUsername},
                                               'target': {
                                                   'lat': calledLat,
                                                   'lng': calledLng}
                                           },
                                           'updatedData': {
                                               'dailyCalls': dailyCalls,
                                               'weeklyCalls': weeklyCalls,
                                               'alltimeCalls': alltimeCalls,
                                               'dailyLeaderboard':dailyLeaderboard
                                           }
                                       }
                                       })

        send_message(websocketMessage)
        return HttpResponse(200)


class api_test_simulateachievement(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if settings.DEBUG == False:
            raise Http404

        achievements = Achievement.objects.all()
        nb = achievements.count()
        achievement = achievements[random.randint(0, nb - 1)]

        websocketMessage = json.dumps({'type': 'achievement',
                                       'value': {
                                           'agentUsername': 'Jean-René',
                                           'achievement': {
                                               'name': achievement.name,
                                               'condition': achievement.condition,
                                               'phi': achievement.phi,
                                               'codeName': achievement.codeName
                                           }
                                       }
                                       })
        send_message(websocketMessage)
        return HttpResponse(200)

# /api/current_user/achievements/
class api_user_achievements(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = request.user

        try :
            unlockedAchievements = user.UserExtend.get_achievements()

        except UserExtend.DoesNotExist:
            unlockedAchievements = []

        data = {}

        #Recuperation des achivements débloqués
        dataUnlockedAchievements = []
        idList = []
        for achievement in unlockedAchievements:
            dataUnlockedAchievements.append({'name':achievement.name,
                                             'condition':achievement.condition,
                                             'phi':achievement.phi,
                                             'codeName':achievement.codeName
                                             })
            idList.append(achievement.id)

        #Recuperation des achivements restants
        lockedAchievements = Achievement.objects.all().exclude(id__in=idList)

        dataLockedAchievements = []
        for achievement in lockedAchievements:
            dataLockedAchievements.append({'name':achievement.name, 'condition':achievement.condition, 'phi':achievement.phi})

        data['unlocked'] = dataUnlockedAchievements[::-1]
        data['locked'] = dataLockedAchievements
        data = json.dumps(data)

        return HttpResponse(data)


# /api/leaderboard/X/ avec X = alltime ou weekly ou daily
class api_leaderboard(APIView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(cache_page(60))
    def get(self, request):

        alltime, weekly,daily = generate_leaderboards(50)

        data = {
                'alltime':alltime,
                'weekly':weekly,
                'daily':daily
                }
        data = json.dumps(data)

        print("recalculated")

        return HttpResponse(data)


# /api/basic_information/
class api_basic_information(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        r = redis.StrictRedis(connection_pool=redis_pool)
        dailyCalls = int(r.get('melenphone:call_count:daily:' + format_date(timezone.now())) or 0)
        weeklyCalls = int(r.get('melenphone:call_count:weekly:' + format_date(timezone.now())) or 0)
        alltimeCalls = int(r.get('melenphone:call_count:alltime') or 0)

        ranking = r.zrevrange('melenphone:leaderboards:daily:' + format_date(timezone.now()), 0, 9, withscores=True)
        dailyLeaderboard = []
        for ranked in ranking:
            try:
                username = User.objects.get(id=int(ranked[0])).UserExtend.agentUsername
            except User.DoesNotExist:
                username = "Unknown"
            calls = int(ranked[1])
            dailyLeaderboard.append({'username': username, 'calls': calls})

        data = {
                'dailyCalls':dailyCalls,
                'weeklyCalls':weeklyCalls,
                'alltimeCalls':alltimeCalls,
                'dailyLeaderboard': dailyLeaderboard
                }
        data = json.dumps(data)

        return HttpResponse(data)


class UserAPI(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_serializer(self, *args, **kwargs):
        return super(UserAPI, self).get_serializer(*args, **kwargs)

    def get_object(self):
        return self.request.user


class CallerInformationAPI(RetrieveAPIView, CreateModelMixin):
    serializer_class = UserExtendSerializer

    def get_object(self):
        try:
            return self.request.user.UserExtend
        except UserExtend.DoesNotExist:
            raise Http404

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    def post(self, request, *args, **kwargs):
        try:
            # try accessing UserExtend related property to see if it exists
            userExtend = request.user.UserExtend
            raise CallerCreationError("Impossible de créer un agent si l'utilisateur en possède déjà un", code='already_exists')
        except UserExtend.DoesNotExist:
            return self.create(request, *args, **kwargs)

class AssociateExistingCallerAgentAPI(CreateAPIView):
    serializer_class = CallhubCredentialsSerializer

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            # try accessing UserExtend related property to see if it exists
            userExtend = request.user.UserExtend
            raise CallerValidationError("Impossible de lier un agent si l'utilisateur en possède déjà un", code='already_exists')
        except UserExtend.DoesNotExist:
            return super(CreateAPIView, self).create(request, *args, **kwargs)