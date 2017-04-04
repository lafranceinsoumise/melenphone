from django.utils import timezone
from melenchonPB.redis import get_redis_instance, format_date
import datetime
import redis

from .leaderboard import generate_leaderboard


def update_scores(user, tzdate=None):
    r = get_redis_instance()
    pipe = r.pipeline(transaction=False)

    # Cles necessaires :
    if tzdate is None:
        tzdate = timezone.now()
    today = format_date(tzdate)

    sevenPreviousDays = [today]
    for i in range(6):
        tzdate += datetime.timedelta(days=1)
        sevenPreviousDays.append(format_date(tzdate))

    # Global counters
    pipe.incr('melenphone:call_count:alltime')

    for day in sevenPreviousDays:
        pipe.incr('melenphone:call_count:weekly:' + day)

    pipe.incr('melenphone:call_count:daily:' + today)

    # Leaderboards
    if not(user is None):
        pipe.zincrby('melenphone:leaderboards:alltime',str(user.id))

        for day in sevenPreviousDays:
            pipe.zincrby('melenphone:leaderboards:weekly:' + day, str(user.id))

        pipe.zincrby('melenphone:leaderboards:daily:' + today, str(user.id))

    pipe.execute()


def get_global_scores():
    r = get_redis_instance()
    daily_calls = int(r.get('melenphone:call_count:daily:' + format_date(timezone.now())) or 0)
    weekly_calls = int(r.get('melenphone:call_count:weekly:' + format_date(timezone.now())) or 0)
    alltime_calls = int(r.get('melenphone:call_count:alltime') or 0)
    daily_leaderboard = generate_leaderboard('daily', 10)

    return {
        'dailyCalls': daily_calls,
        'weeklyCalls': weekly_calls,
        'alltimeCalls': alltime_calls,
        'dailyLeaderboard': daily_leaderboard
    }
