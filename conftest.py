import pprintpp
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from django.test.client import Client

from items.models import Category, Item

fake = Faker()
User = get_user_model()


@pytest.fixture(scope='session')
def faker():
    # global fake
    yield fake


@pytest.fixture(scope='function')
def user(db):
    user, _ = User.objects.get_or_create(
        email='user1@gmail.com',
        first_name='John',
        phone='123456789',
        is_phone_valid=True
    )
    user.set_password('123456789')
    user.save()
    yield user


@pytest.fixture(scope='function')
def login_user(db):
    email = 'user1@gmail.com'
    phone = '123456789'
    password = '123456789'
    user, _ = User.objects.get_or_create(
        email=email,
        first_name='John',
        phone=phone,
        is_phone_valid=True
    )
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'), data={'username': email, 'password': password})

    assert response.status_code == 302
    yield client, user


@pytest.fixture(scope='function')
def item(db):
    category = Category.objects.create(
        name='Water'
    )

    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open('C:/IT/drinks.jpg', 'rb').read(),
        content_type='image/jpeg'
    )

    item = Item.objects.create(
        name='Borjomi 0.5 L',
        category=category,
        image=image
    )
    yield item


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    __builtins__['pp'] = pprintpp.PrettyPrinter(width=41)
    # code before tests run
    yield
    del __builtins__['pp']
    # code after tests run


@pytest.fixture(scope='session')
def celery_task_always_eager(celery_worker):
    return True
