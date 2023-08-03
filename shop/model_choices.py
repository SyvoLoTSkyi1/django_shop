from django.db.models import IntegerChoices, TextChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'Value'
    PERCENT = 1, 'Percent'


class Currency(TextChoices):
    UAH = 0, 'UAH'
    USD = 1, 'USD'
    EUR = 2, 'EUR'
