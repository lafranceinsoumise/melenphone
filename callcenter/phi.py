# -*- coding: utf-8 -*-
#Django imports
from django.utils import timezone

#Python imports
import datetime
from decimal import *

#Project imports
from callcenter.models import *

BASE_PHI = 10

MIN_DELAY = 60
MULTIPLIER_RESET = 3600

PHI_FIRST_CALL = 50
MULTIPLIER_GROWTH = Decimal('0.1')
MAX_MULTIPLIER = 3


def EarnPhi(username):
    if UserExtend.objects.filter(agentUsername=username).exists(): #On check si le user existe
        user = UserExtend.objects.filter(agentUsername=username)[0].user

        #On récupère ses appels
        calls = Appel.objects.filter(user=user)

        #A partir de là on travaille sur le userExtend
        user = user.UserExtend

        #On vérifie qu'il n'a pas passé un appel trop récement
        if len(calls) == 0: #Si le user n'a jamais appelé
            authorization = True
        else:
            calls = calls.order_by('-date')
            lastCall = calls[0].date
            if (timezone.now() - lastCall).seconds > MIN_DELAY:
                authorization = True
            else:
                authorization = False #Si le dernier appel est trop récent (<60s), on s'arrête

        if authorization:
            if len(calls) == 0: #Cas particulier où le user est nouveau
                user.phi = user.phi + BASE_PHI + PHI_FIRST_CALL
                user.phi_multiplier = user.phi_multiplier + MULTIPLIER_GROWTH
                user.first_call_of_the_day = timezone.now()
                user.save()
            else: #Cas général
                #ETAPE 1 : On vérifie si on doit reset le multiplier
                if (timezone.now() - lastCall).seconds > MULTIPLIER_RESET:
                    user.phi_multiplier = 1

                #ETAPE 2 : Le joueur gagne des phis
                user.phi = user.phi + (BASE_PHI * user.phi_multiplier)

                #ETAPE 3 : On augmente le multiplier et on vérifie qu'il ne dépasse pas le max
                user.phi_multiplier = min(user.phi_multiplier + MULTIPLIER_GROWTH, MAX_MULTIPLIER)

                #ETAPE 4 : On regarde si on doit accorder le premier appel du jour
                if (timezone.now() - user.first_call_of_the_day).seconds > 3600*24:
                    user.phi = user.phi + PHI_FIRST_CALL
                    user.first_call_of_the_day = timezone.now()

                #On sauvegarde tout ça !
                user.save()
                #On ajoute l'appel à la bdd
            if UserExtend.objects.filter(agentUsername=username).exists(): #Si le user est inscrit sur le site
                userToSave = UserExtend.objects.filter(agentUsername=username)[0].user
                Appel.objects.create(user=userToSave) #On enregistre l'appel et son id
            else: #Si on ne connait pas le user
                Appel.objects.create() #On enregistre quand même l'appel (pour les stats)
