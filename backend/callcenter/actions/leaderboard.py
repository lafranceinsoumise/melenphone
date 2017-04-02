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

    redis_leaderboard = get_leaderboard(period, top)

    id_list = [item[0] for item in redis_leaderboard]

    users = User.objects.filter(id__in=id_list)

    leaderboard = []
    for ranked in redis_leaderboard:
        try:
            user = next(user for user in users if user.id == int(ranked[0]))
            username = user.UserExtend.agentUsername
            calls = int(ranked[1])
            leaderboard.append({'username': username, 'calls': calls})
        except User.DoesNotExist:
            pass
        except UserExtend.DoesNotExist:
            pass
        except StopIteration:
            pass

    return leaderboard


def get_leaderboard(period, top):
    r = redis.StrictRedis(connection_pool=redis_pool)
    if period == 'alltime':
        return r.zrevrange('melenphone:leaderboards:alltime',
                           0,
                           top-1,
                           withscores=True)
    else:
        return r.zrevrange('melenphone:leaderboards:' + period + ':' + format_date(timezone.now()),
                           0,
                           top-1,
                           withscores=True)
