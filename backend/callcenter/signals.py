from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Call
from .actions.achievements import update_achievements
from .actions.score import update_scores


@receiver(post_save, sender=Call, dispatch_uid='call_post_save_update_scores')
def call_post_save(instance, created, raw, **kwargs):
    """
    Update scores, phis and leaderboard when a call is created
    
    :param instance: the created or updated model instance
    :param created: whether the instance was created or updated
    :param raw: whether the db is in raw mode, in this case we cannot access the user
    :return: 
    """

    # we check that the call is created, and we are not in raw mode
    if created and not raw:
        user = instance.user

        update_scores(user)
        update_achievements(user)

    pass
