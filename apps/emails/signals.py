from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Email
from .tasks import task_send_emails


@receiver(post_save, sender=Email)
def send_emails(sender, instance, created, **kwargs):
    if created:
        if instance.send_time:
            eta = instance.send_time - timezone.now()
        else:
            eta = 5
        task_send_emails.apply_async(args=[instance.id], countdown=eta)
