import redis
from redis.connection import UnixDomainSocketConnection
from django.conf import settings
from django.utils import timezone


if settings.REDIS_UNIX_SOCKET is not None:
    redis_pool = redis.ConnectionPool(
        connection_class=UnixDomainSocketConnection,
        path=settings.REDIS_UNIX_SOCKET,
        max_connections=settings.REDIS_MAX_CONNECTIONS
    )
else:
    redis_pool = redis.ConnectionPool(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, max_connections=settings.REDIS_MAX_CONNECTIONS
    )


def format_date(date):
    return (str(date.year) + '/' + str(date.month) + '/' + str(date.day))

def get_leaderboard(type, top):
    r = redis.StrictRedis(connection_pool=redis_pool)
    if type == 'alltime':
        return r.zrevrange('melenphone:leaderboards:alltime', 0, top-1, withscores=True)
    else:
        return r.zrevrange('melenphone:leaderboards:' + type + ':' + format_date(timezone.now()), 0, top-1, withscores=True)