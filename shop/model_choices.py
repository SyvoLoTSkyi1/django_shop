from django.db.models import IntegerChoices


class DiscountTypes(IntegerChoices):
    VALUE = 0, 'Value'
    PERCENT = 1, 'Percent'
