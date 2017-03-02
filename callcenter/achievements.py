# -*- coding: utf-8 -*-

#Django imports

#Project import
from callcenter.models import *

#Python imports

#Fonction principale
def updateAchievements(agentUsername):
    if UserExtend.objects.filter(agentUsername=username).exists(): #On check si le user existe
        user = UserExtend.objects.filter(agentUsername=username)[0].user
        #Appeler les autres fonctions
