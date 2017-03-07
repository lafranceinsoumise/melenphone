# -*- coding: utf-8 -*-

#Django imports
from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View, TemplateView
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_jwt import views
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

#Python imports
import requests
import json

#Project imports
from callcenter.models import *
from callcenter.map import *
from callcenter.phi import *
from callcenter.consumers import *
from .forms import *

#JWT auth


class AngularApp(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(AngularApp, self).get_context_data(**kwargs)
        context['ANGULAR_URL'] = settings.ANGULAR_URL
        return context

class SampleView(View):
    """View to render django template to angular"""
    def get(self, request):
        return HttpResponse("OK!")

class NgTemplateView(View):
    """View to render django template to angular"""
    def get(self, request):
        return render(request, 'template.html', {"django_variable": "This is django context variable"})

@require_POST
@csrf_exempt #Sinon la requete est bloquée car lancée depuis un autre site (donc qui n'a pas le cookie csrf)
def noteWebhook(request):
    jsondata = request.body
    data = json.loads(jsondata)

    #Latitude et longitude de l'appelant
    callerAgentUsername = data['data']['agent']['username']
    callerLat, callerLng = getCallerLocation(callerAgentUsername)

    #Latitude et longitude de l'appellé
    calledNumber = data['data']['contact']
    calledLat, calledLng = getCalledLocation(calledNumber)

    #On crédite les phis que gagne le user
    EarnPhi(callerAgentUsername)

    #On ajoute l'appel à la bdd
    if UserExtend.objects.filter(agentUsername=callerAgentUsername).exists(): #Si le user est inscrit sur le site
        userToSave = UserExtend.objects.filter(agentUsername=callerAgentUsername)[0].user
        Appel.objects.create(user=userToSave) #On enregistre l'appel et son id
    else: #Si on ne connait pas le user
        Appel.objects.create() #On enregistre quand même l'appel (pour les stats)

    #On met à jour les achievements
    updateAchievements(callerAgentUsername)

    #On envoie les positions au websocket pour l'animation
    websocketMessage = json.dumps({
        'caller':{'lat':callerLat, 'lng':callerLng},
        'target':{'lat':calledLat, 'lng':calledLng}
    })
    send_message(websocketMessage)
    return HttpResponse(status=200)

def index(request):
    return render(request, 'callcenter/index.html', locals())


# View pour l'enregistrement d'un nouveau membre et création de son agent callhub
def registerNew(request):
    if request.method == 'POST':
        form = registerNewForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            country=form.cleaned_data['country']
            city=form.cleaned_data['city']

            address = city + '+' + country
            address.replace(" ", "+")

            token = 'Token ' + settings.CALLHUB_API_KHEY
            headers = {'Authorization': token }
            data = {'username':username, 'email':email, 'team':'tout_le_monde'}
            r = requests.post('https://api.callhub.io/v1/agents/', data=data, headers=headers) #On fait la requete sur l'API de github
            if r.status_code == requests.codes.created: #Si tout s'est bien passé
                #On crée le user dans la bdd
                user,created = User.objects.get_or_create(username=username, email=email) #On tente de créer le user
                if created:
                    user.set_password(password)
                    user.save()
                    #On crée alors la partie userextend
                    date = timezone.now()
                    date.replace(year = date.year-1)
                    userExtend, created = UserExtend.objects.get_or_create(agentUsername=username, address=address, first_call_of_the_day = date, user=user, phi=0, phi_multiplier=1.0)
                    if created:
                        userExtend.save()
                        return redirect('register_sucess')
                    else: #Si y'a un problème, on supprime le User créé juste avant
                        user.delete()
                        form.add_error(None, "Une erreur est survenue.")
                else:
                    form.add_error(None, "Une erreur est survenue.")
            elif r.status_code == 400: #Bad request : le username existe déjà !
                form.add_error('username', "Ce nom d'utilisateur est déjà utilisé sur Callhub !")
            else: #Autre erreur de callhub
                form.add_error(None, "Callhub ne répond pas, veuillez réessayer plus tard.")
    else:
        form=registerNewForm()
    return render(request, 'callcenter/register.html', locals())

#View de transition après enregistrement d'un nouvel utilisateur
def registerSucess(request):
    return render(request, 'callcenter/register_success.html', locals())

#### REST API


class api_test_socket(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        send_message(request.body)
        return HttpResponse(200)

class api_test_simulatecall(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):

        callerLat, callerLng = randomLocation()
        calledLat, calledLng = randomLocation()

        websocketMessage = json.dumps({
            'caller':{'lat':callerLat, 'lng':callerLng},
            'target':{'lat':calledLat, 'lng':calledLng}
        })

        send_message(websocketMessage)

        return HttpResponse(200)

class api_user_infos(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        user = request.user

        username = user.username

        userExtend = user.UserExtend
        phi = userExtend.phi
        phi_multiplier = userExtend.phi_multiplier
        alltime_leaderboard = userExtend.alltime_leaderboard
        weekly_leaderboard = userExtend.weekly_leaderboard
        daily_leaderboard = userExtend.daily_leaderboard


        data = json.dumps({     'username': username,
                                'phi': str(phi),
                                'phi_multiplier':str(phi_multiplier),
                                'leaderboard':{     'alltime':str(alltime_leaderboard),
                                                    'weekly':str(weekly_leaderboard),
                                                    'daily':str(daily_leaderboard)}
                        })

        return HttpResponse(data)

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

class api_leaderboard(APIView):
    permission_classes = (permissions.AllowAny,)
