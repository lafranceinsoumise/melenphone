from melenchonPB.redis import redis_pool, format_date
from accounts.models import User
from callcenter.models import UserExtend
import redis
from django.utils import timezone


def generate_leaderboards(top):
    alltime = generate_leaderboard('alltime', top)
    weekly = generate_leaderboard('weekly', top)
    daily = generate_leaderboard('daily', top)

    return alltime, weekly, daily


def generate_leaderboard(period, top):
    redis_leaderboard = get_leaderboard_from_redis(period, top)
    user_pks = [int(pk_as_str) for pk_as_str, score_as_str in redis_leaderboard]
    users = User.objects.filter(pk__in=user_pks)
    users_map = {u.pk: u for u in users}

    leaderboard = []

    for pk_as_str, score_as_str in redis_leaderboard:
        try:
            username = users_map[int(pk_as_str)].UserExtend.agentUsername
        except (KeyError, UserExtend.DoesNotExist):
            username = "???"
        score = int(score_as_str)

        leaderboard.append({
            'username': username,
            'calls': score
        })

    return leaderboard


def get_leaderboard_from_redis(period, top):
    r = redis.StrictRedis(connection_pool=redis_pool)
    if period == 'alltime':
        return r.zrevrange(
            'melenphone:leaderboards:alltime',
            0,
            top - 1,
            withscores=True
        )
    else:
        return r.zrevrange(
            'melenphone:leaderboards:' + period + ':' + format_date(timezone.now()),
            0,
            top - 1,
            withscores=True
        )
