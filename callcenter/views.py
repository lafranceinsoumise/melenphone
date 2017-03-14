# -*- coding: utf-8 -*-

import json
import redis
#Django imports
from django.utils import timezone

from django.conf import settings
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.mixins import CreateModelMixin
from django.http import Http404

#Project imports
from callcenter.models import *
from accounts.models import User
from callcenter.achievements import updateAchievements
from callcenter.map import getCallerLocation, getCalledLocation, randomLocation
from callcenter.phi import EarnPhi
from callcenter.consumers import send_message
from callcenter.serializers import UserSerializer, UserExtendSerializer
from callcenter.exceptions import CallerCreationError
from melenchonPB.redis import redis_pool, format_date
from callcenter.actions.score import update_scores

#ANGULAR APP
class AngularApp(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(AngularApp, self).get_context_data(**kwargs)
        context['ANGULAR_URL'] = settings.ANGULAR_URL
        return context

#################### WEBHOOKS ################################

# /api/simulate_call/
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

            #On ajoute l'appel au serveur redis
            update_scores(user)

            #On ajoute l'appel à la bdd pour pouvoir reconstruire redis si besoin
            Call.objects.create(user=user)

            #On met à jour les achievements
            updateAchievements(user)

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

            websocketMessage = json.dumps({ 'type':'call',
                                            'values':{
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
                                                    'alltimeCalls':alltimeCalls
                                                    }
                                            }
                                        })
            send_message(websocketMessage)

        return HttpResponse(status=200)


#################### REST API ################################

# /api/test_websocket/
class api_test_socket(APIView):
    if settings.DEBUG == False:
        raise Http404
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        send_message(request.body)
        return HttpResponse(200)


# /api/simulate_call/
class api_test_simulatecall(APIView):
    if settings.DEBUG == False:
        raise Http404
    permission_classes = (permissions.AllowAny,)
    def post(self, request):

        callerLat, callerLng = randomLocation()
        calledLat, calledLng = randomLocation()

        update_scores(None)
        Call.objects.create()

        r = redis.StrictRedis(connection_pool=redis_pool)
        dailyCalls = int(r.get('melenphone:call_count:daily:' + format_date(timezone.now())) or 0)
        weeklyCalls = int(r.get('melenphone:call_count:weekly:' + format_date(timezone.now())) or 0)
        alltimeCalls = int(r.get('melenphone:call_count:alltime') or 0)

        websocketMessage = json.dumps({'type': 'call',
                                       'values': {
                                           'call': {
                                               'caller': {
                                                   'lat': callerLat,
                                                   'lng': callerLng,
                                                   'id': None,
                                                   'agentUsername': None},
                                               'target': {
                                                   'lat': calledLat,
                                                   'lng': calledLng}
                                           },
                                           'updatedData': {
                                               'dailyCalls': dailyCalls,
                                               'weeklyCalls': weeklyCalls,
                                               'alltimeCalls': alltimeCalls
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
        unlockedAchievements = user.UserExtend.get_achievements()

        data = {}

        #Recuperation des achivements débloqués
        dataUnlockedAchievements = []
        idList = []
        for achievement in unlockedAchievements:
            dataUnlockedAchievements.append({'name':achievement.name, 'condition':achievement.condition})
            idList.append(achievement.id)

        #Recuperation des achivements restants
        lockedAchievements = Achievement.objects.all().exclude(id__in=idList)

        dataLockedAchievements = []
        for achievement in lockedAchievements:
            dataLockedAchievements.append({'name':achievement.name, 'condition':achievement.condition})

        data['unlocked'] = dataUnlockedAchievements
        data['locked'] = dataLockedAchievements
        data = json.dumps(data)

        return HttpResponse(data)


# /api/leaderboard/X/ avec X = alltime ou weekly ou daily
class api_leaderboard(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, ranking):
        r = redis.StrictRedis(connection_pool=redis_pool)
        #URL "alltime" -> On récupère le leaderboard alltime
        if ranking == "alltime":
            ranking = r.zrange('melenphone:leaderboards:alltime',0,49,withscores=True)
            usersTab = []
            for ranked in ranking:
                username = User.objects.filter(id=int(ranked[0]))[0].UserExtend.agentUsername
                calls = int(ranked[1])
                usersTab.append({'username':username, 'calls':str(calls)})

        #URL "weekly" -> On récupère le leaderboard weekly
        elif ranking == "weekly":
            ranking = r.zrange('melenphone:leaderboards:weekly:' + format_date(timezone.now()),0,49,withscores=True)
            usersTab = []
            for ranked in ranking:
                username = User.objects.filter(id=int(ranked[0]))[0].UserExtend.agentUsername
                calls = int(ranked[1])
                usersTab.append({'username':username, 'calls':str(calls)})

        #URL "daily" -> On récupère le leaderboard daily
        elif ranking == "daily":
            ranking = r.zrange('melenphone:leaderboards:daily:' + format_date(timezone.now()),0,49,withscores=True)
            usersTab = []
            for ranked in ranking:
                username = User.objects.filter(id=int(ranked[0]))[0].UserExtend.agentUsername
                calls = int(ranked[1])
                usersTab.append({'username':username, 'calls':str(calls)})

        #Ne correspond à aucun leaderboard -> 404
        else:
            raise Http404

        data = {'leaderboard':usersTab}
        data = json.dumps(data)

        return HttpResponse(data)


# /api/basic_information/
class api_basic_information(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):
        r = redis.StrictRedis(connection_pool=redis_pool)
        dailyCalls = int(r.get('melenphone:call_count:daily:' + format_date(timezone.now())) or 0)
        weeklyCalls = int(r.get('melenphone:call_count:weekly:' + format_date(timezone.now())) or 0)
        alltimeCalls = int(r.get('melenphone:call_count:alltime') or 0)

        data = {
                'dailyCalls':dailyCalls,
                'weeklyCalls':weeklyCalls,
                'alltimeCalls':alltimeCalls
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
            raise CallerCreationError('Cannot create new agent if user already has one', code='already_exists')
        except UserExtend.DoesNotExist:
            return self.create(request, *args, **kwargs)
