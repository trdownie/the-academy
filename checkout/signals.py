from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Order

@receiver(post_save, sender=Order)
def update_on_save(sender, instance, created, **kwargs):
    """
    Update order total on lineitem update/create
    """
    instance.update_total()

@receiver(post_delete, sender=Order)
def update_on_delete(sender, instance, **kwargs):
    """
    Update order total on lineitem delete
    """
    instance.update_total()