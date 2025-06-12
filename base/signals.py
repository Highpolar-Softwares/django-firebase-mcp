from django.dispatch import receiver, Signal
from django.db.models.signals import post_save, post_delete, m2m_changed
from .models import Activity


@receiver(post_save)
def my_callback(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        Activity.objects.create(
            content_object=instance, operation=Activity.OperationChoiceSet.CREATED
        )
    else:
        Activity.objects.create(
            content_object=instance, operation=Activity.OperationChoiceSet.UPDATED
        )
