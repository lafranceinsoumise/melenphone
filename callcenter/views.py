# -*- coding: utf-8 -*-

#Django imports
from django.http import HttpResponse
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateAPIView
from django.http import Http404

#Project imports
from callcenter.achievements import *
from callcenter.map import *
from callcenter.phi import *
from callcenter.consumers import *
from callcenter.serializers import UserExtendSerializer
from .forms import *


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
        MIN_DELAY = 60

        jsondata = request.body
        data = json.loads(jsondata)

        #Latitude et longitude de l'appelant
        callerAgentUsername = data['data']['agent']['username']
        callerLat, callerLng = getCallerLocation(callerAgentUsername)

        #Latitude et longitude de l'appellé
        calledNumber = data['data']['contact']
        calledLat, calledLng = getCalledLocation(calledNumber)

        try:
            user = UserExtend.objects.get(agentUsername=callerAgentUsername).user #On le récupère

            calls = Appel.objects.filter(user=user)
            #On vérifie qu'il n'a pas passé un appel trop récement
            if len(calls) == 0: #Si le user n'a jamais appelé
                authorization = True
                lastCall = None
            else:
                calls = calls.order_by('-date')
                lastCall = calls[0].date
                if (timezone.now() - lastCall).seconds > MIN_DELAY:
                    authorization = True
                else:
                    authorization = False #Si le dernier appel est trop récent (<60s), on s'arrête

            if authorization: #Si le dernier appel n'est pas trop recent
                #On crédite les phis que gagne le user
                EarnPhi(callerAgentUsername, lastCall)

                #On enregistre l'appel avec le user associé
                Appel.objects.create(user=user)

                #On ajoute l'appel au décompte du jour
                dcalls = PrecomputeData.objects.filter(code="dcalls")[0]
                dcalls.integer_value += 1
                dcalls.save()


                #On met à jour les achievements
                updateAchievements(user)

                #On envoie les positions au websocket pour l'animation
                websocketMessage = json.dumps({ 'call': {
                                                        'caller': {
                                                            'lat':callerLat,
                                                            'lng':callerLng,
                                                            'id':user.id,
                                                            'username':user.username},
                                                        'target': {
                                                            'lat':calledLat,
                                                            'lng':calledLng}
                                                        },
                                                'updatedData': {
                                                        'dailyCalls':dcalls.integer_value
                                                        }
                })
                send_message(websocketMessage)

        #Si on ne connait pas l'agent callhub
        except UserExtend.DoesNotExist:
            Appel.objects.create() #On enregistre quand même l'appel (pour les stats)

            #On ajoute 1 au compteur des appels du jour
            # TODO: race condition here
            dcalls = PrecomputeData.objects.filter(code="dcalls")[0]
            dcalls.integer_value += 1
            dcalls.save()

            #On envoie les positions au websocket pour l'animation
            websocketMessage = json.dumps({ 'call': {
                                                    'caller': {'lat':callerLat, 'lng':callerLng, 'id':0, 'username':callerAgentUsername},
                                                    'target': {'lat':calledLat, 'lng':calledLng}
                                                    },
                                            'updatedData': {
                                                    'dailyCalls':dcalls.integer_value
                                                    }
            })
            send_message(websocketMessage)
        return HttpResponse(status=200)


#################### REST API ################################

# /api/test_websocket/
class api_test_socket(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        send_message(request.body)
        return HttpResponse(200)


# /api/simulate_call/
class api_test_simulatecall(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):

        callerLat, callerLng = randomLocation()
        calledLat, calledLng = randomLocation()
        dcalls = PrecomputeData.objects.filter(code="dcalls")[0].integer_value

        websocketMessage = json.dumps({ 'call': {
                                                'caller': {'lat':callerLat, 'lng':callerLng},
                                                'target': {'lat':calledLat, 'lng':calledLng}
                                                },
                                        'updatedData': {
                                                'dailyCalls':dcalls
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
        users = UserExtend.objects.all()

        #URL "alltime" -> On récupère le leaderboard alltime
        if ranking == "alltime":
            users = users.filter(alltime_leaderboard__gte=1).order_by('alltime_leaderboard')
            usersTab = []
            for user in users:
                username = user.user.username
                calls = user.alltime_leaderboard_calls
                usersTab.append({'username':username, 'calls':str(calls)})

        #URL "weekly" -> On récupère le leaderboard weekly
        elif ranking == "weekly":
            users = users.filter(weekly_leaderboard__gte=1).order_by('weekly_leaderboard')
            usersTab = []
            for user in users:
                username = user.user.username
                calls = user.weekly_leaderboard_calls
                usersTab.append({'username':username, 'calls':str(calls)})

        #URL "daily" -> On récupère le leaderboard daily
        elif ranking == "daily":
            users = users.filter(daily_leaderboard__gte=1).order_by('daily_leaderboard')
            usersTab = []
            for user in users:
                username = user.user.username
                calls = user.daily_leaderboard_calls
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

        dcalls = PrecomputeData.objects.get(code="dcalls").integer_value

        data = {'dailyCalls': dcalls}
        data = json.dumps(data)

        return HttpResponse(data)


class UserAPI(RetrieveUpdateAPIView):
    serializer_class = UserExtendSerializer

    def get_object(self):
        try:
            return self.request.user.UserExtend
        except UserExtend.DoesNotExist:
            return UserExtend(user=self.request.user)