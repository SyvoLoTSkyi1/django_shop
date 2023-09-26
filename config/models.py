from django.db import models

from shop.settings import env


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Config(SingletonModel):
    contact_form_email = models.EmailField(env('ADMIN_EMAIL', default='ADMIN_EMAIL'))
