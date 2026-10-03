from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Message, Notification


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):

    if not created:
        return

    if instance.sender == instance.receiver:
        return

    Notification.objects.create(
        user=instance.receiver,
        sender=instance.sender,
        message=instance,
        text=f'{instance.sender.username} написал вам по объявлению "{instance.post.title}"'
    )