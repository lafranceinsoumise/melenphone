from django.utils import timezone
from melenchonPB.redis_pool import redis_pool
import datetime
import redis

def update_scores(user):
    r = redis.StrictRedis(connection_pool=redis_pool)

    # Cles necessaires :
    tzdate = timezone.now()
    today = str(tzdate.year) + '/' + str(tzdate.month) + '/' + str(tzdate.day)
    sevenPreviousDays = [today]
    for i in range(6):
        tzdate -= datetime.timedelta(days=1)
        sevenPreviousDays.append(str(tzdate.year) + '/' + str(tzdate.month) + '/' + str(tzdate.day))

    # Global counters
    r.incr('call_count:alltime')

    for day in sevenPreviousDays:
        r.incr('call_count:weekly:' + day)

    r.incr('call_count:daily:' + today)



    # Leaderboards
    r.zincrby('leaderboards:alltime',str(user.id))

    for day in sevenPreviousDays:
        r.incr('leaderboards:weekly:' + day, str(user.id))

    r.incr('leaderboards:daily:' + today, str(user.id))

