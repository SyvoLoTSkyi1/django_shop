import logging

from celery import shared_task

from currencies.models import CurrencyHistory
from items.models import Item

logger = logging.getLogger(__name__)


@shared_task
def update_price():
    currency_list = CurrencyHistory.objects.order_by('-created_at').values(
        'currency', 'sale')[:2]

    for items in Item.objects.iterator():
        try:
            if items.currency == currency_list[0]['currency']:
                items.actual_price = items.price * currency_list[0][
                    'sale']
            elif items.currency == currency_list[1]['currency']:
                items.actual_price = items.price * currency_list[1][
                    'sale']
            else:
                items.actual_price = items.price
            items.save(update_fields=['actual_price'])
        except (KeyError, ValueError) as error:
            logger.error(error)


