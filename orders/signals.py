from django.db.models.signals import pre_save
from django.dispatch import receiver

from orders.models import Order


# @receiver(pre_save, sender=Order)
# def pre_save_order(sender, signal, instance, **kwargs):
#     instance.total_amount = instance.get_total_amount()