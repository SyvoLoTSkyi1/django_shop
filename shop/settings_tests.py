from .settings import *
from faker import Faker

fake = Faker()


REMOVE_MIDDLEWARE = ['silk.middleware.SilkyMiddleware']
for i in REMOVE_MIDDLEWARE:
    try:
        MIDDLEWARE.remove(i)
    except IndexError:
        ...


CELERY_TASK_ALWAYS_EAGER = True
