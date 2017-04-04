from django_redis import get_redis_connection


def get_redis_instance():
    return get_redis_connection()


def format_date(date):
    return (str(date.year) + '/' + str(date.month) + '/' + str(date.day))
