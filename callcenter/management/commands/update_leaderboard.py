#Django imports
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
from django.contrib.auth.models import User

#Python imports

#Project import
from callcenter.models import Appel, UserExtend

class Command(BaseCommand):
    def handle(self, *args, **options):

        #On reset les placements
        UserExtend.objects.all().update(daily_leaderboard=0, weekly_leaderboard=0, alltime_leaderboard=0)

        #Mise à jour du alltime_leaderboard
        leaders = Appel.objects.values('user').annotate(Count('user')).order_by('-user__count')

        for index, leader in enumerate(leaders):
            userID = leader['user']
            userExtend = User.objects.filter(id=userID)[0].UserExtend
            userExtend.alltime_leaderboard = index + 1
            userExtend.save()

        #Mise à jour du weekly_leaderboard
        
