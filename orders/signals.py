from django.db.models.signals import pre_save  # noqa
from django.dispatch import receiver  # noqa

from orders.models import Order  # noqa


@receiver(pre_save, sender=Order)
def pre_save_order(sender, signal, instance, **kwargs):
    instance.total_amount = instance.get_total_amount()
