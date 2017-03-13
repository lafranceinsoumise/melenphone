# -*- coding: utf-8 -*-
#Python imports
from decimal import Decimal
from django.utils import timezone

BASE_PHI = 10

MULTIPLIER_RESET = 3600

PHI_FIRST_CALL = 50
MULTIPLIER_GROWTH = Decimal('0.1')
MAX_MULTIPLIER = 3


def EarnPhi(user, lastCall):
    user = user.UserExtend

    if lastCall is None: #Cas particulier où le user est nouveau
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
