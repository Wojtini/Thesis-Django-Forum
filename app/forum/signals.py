from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from forum.models import Review


@receiver(post_save, sender=Review)
def post_message_rating_update(sender, instance: Review, created, **kwargs):
    if not created:
        instance.entry.update_date = timezone.now()
        instance.save()
