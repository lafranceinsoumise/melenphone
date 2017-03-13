from django.utils import timezone
from melenchonPB.redis_pool import redis_pool
import datetime
import redis

def update_scores(user):
    r = redis.StrictRedis(connection_pool=redis_pool)
    pipe = r.pipeline(transaction=False)

    # Cles necessaires :
    tzdate = timezone.now()
    today = str(tzdate.year) + '/' + str(tzdate.month) + '/' + str(tzdate.day)
    sevenPreviousDays = [today]
    for i in range(6):
        tzdate -= datetime.timedelta(days=1)
        sevenPreviousDays.append(str(tzdate.year) + '/' + str(tzdate.month) + '/' + str(tzdate.day))

    # Global counters
    pipe.incr('call_count:alltime')

    for day in sevenPreviousDays:
        pipe.incr('call_count:weekly:' + day)

    pipe.incr('call_count:daily:' + today)



    # Leaderboards
    if not(user is None):
        pipe.zincrby('leaderboards:alltime',str(user.id))

        for day in sevenPreviousDays:
            pipe.zincrby('leaderboards:weekly:' + day, str(user.id))

        pipe.zincrby('leaderboards:daily:' + today, str(user.id))

    pipe.execute()