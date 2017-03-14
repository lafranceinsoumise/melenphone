from django.core.management.base import BaseCommand, CommandError
from callcenter.models import Call
from callcenter.actions.score import update_scores
from melenchonPB.redis import redis_pool
import redis

class Command(BaseCommand):
    def handle(self, *args, **options):

        r = redis.StrictRedis(connection_pool=redis_pool)
        keys = r.keys('melenphone:*')

        pipe = r.pipeline(transaction=False)

        for key in keys:
            pipe.delete(key)

        pipe.execute()

        for call in Call.objects.all():
            update_scores(call.user)

        print('Base redis reconstruite !')