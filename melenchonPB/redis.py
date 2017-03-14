import redis
from django.conf import settings

redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, max_connections=settings.REDIS_MAX_CONNECTIONS
)

def format_date(date):
    return (str(date.year) + '/' + str(date.month) + '/' + str(date.day))