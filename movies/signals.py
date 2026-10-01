from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Movie
from .push import send_movie_notification


@receiver(post_save, sender=Movie)
def notify_when_movie_is_created(sender, instance, created, **kwargs):
    if not created:
        return

    transaction.on_commit(
        lambda: send_movie_notification(instance)
    )
