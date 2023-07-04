from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models

from shop.mixins.models_mixins import PKMixin


class Feedback(PKMixin):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )

    text = models.TextField()

    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)]
    )

    def __str__(self):
        return f'{self.user.username} | {self.text} | {self.rating}'
