import json
import logging

from django.conf import settings
from pywebpush import WebPushException, webpush

from .models import PushSubscription


logger = logging.getLogger(__name__)


def send_movie_notification(movie):
    private_key_file = settings.VAPID_PRIVATE_KEY_FILE

    if not settings.VAPID_PUBLIC_KEY:
        logger.warning(
            "VAPID public key is not configured. "
            "Movie notification skipped."
        )
        return

    payload = {
        "title": f"New Movie: {movie.title}",
        "body": "A new movie has just been added to FILM SALOON.",
        "url": f"/movie/{movie.slug}/",
        "icon": "/static/icons/icon-192.png",
        "badge": "/static/icons/icon-192.png",
        "tag": f"film-saloon-movie-{movie.pk}",
    }

    subscriptions = PushSubscription.objects.filter(
        active=True
    )

    for subscription in subscriptions:
        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh,
                "auth": subscription.auth,
            },
        }

        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps(payload),
                vapid_private_key=private_key_file,
                vapid_claims={
                    "sub": settings.VAPID_CLAIM_EMAIL,
                },
                ttl=86400,
            )

        except WebPushException as exc:
            status_code = getattr(
                exc,
                "status_code",
                None,
            )

            if status_code in (404, 410):
                logger.info(
                    "Removing expired push subscription %s.",
                    subscription.pk,
                )
                subscription.delete()
            else:
                logger.exception(
                    "Push notification failed for subscription %s: %s",
                    subscription.pk,
                    exc,
                )

        except Exception:
            logger.exception(
                "Unexpected push notification error "
                "for subscription %s.",
                subscription.pk,
            )
