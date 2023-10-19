import csv
import os

import factory
import pprintpp
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from faker import Faker
from django.test.client import Client
from pytest_factoryboy import register

from items.models import Category, Item
from shop.constants import DECIMAL_PLACES

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
def item(db):
    category = Category.objects.create(
        name='guygiuyguy'
    )

    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open('C:/IT/drinks.jpg', 'rb').read(),
        content_type='image/jpeg'
    )

    item = Item.objects.create(
        name=fake.word(),
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


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name', )

    name = factory.Sequence(lambda x: fake.name())
    description = factory.Sequence(lambda x: fake.sentence())
    image = factory.django.ImageField()


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda x: fake.email())
    first_name = factory.Sequence(lambda x: fake.name())
    last_name = factory.Sequence(lambda x: fake.name())


@register
class ItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Item
        django_get_or_create = ('name', 'category',)

    name = factory.Sequence(lambda x: fake.name())
    description = factory.Sequence(lambda x: fake.sentence())
    image = factory.django.ImageField()
    price = factory.Sequence(lambda x: fake.pydecimal(
        min_value=1,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES
    ))
    sku = factory.Sequence(lambda x: fake.word())
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def post_create(self, created, *args, **kwargs):
        if created and not kwargs.get('deny_post'):
            for _ in range(1, 3):
                self.items.add(ItemFactory(post_create__deny_post=True))


@pytest.fixture(scope='function')
def login_user(db):
    phone = '123456789'
    password = '123456789'
    # user, _ = User.objects.get_or_create(
    #     email=email,
    #     first_name='John',
    #     phone=phone,
    #     is_phone_valid=True
    # )
    user = UserFactory(phone=phone, is_phone_valid=True)
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'), data={'username': user.email, 'password': password})

    assert response.status_code == 302
    yield client, user


@pytest.fixture(scope='function')
def login_user_is_staff(db):
    phone = '123456789'
    password = '123456789'
    # user, _ = User.objects.get_or_create(
    #     email=email,
    #     first_name='John',
    #     phone=phone,
    #     is_phone_valid=True
    # )
    user = UserFactory(phone=phone, is_phone_valid=True, is_staff=True)
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'), data={'username': user.email, 'password': password})

    assert response.status_code == 302
    yield client, user


@pytest.fixture(scope='function')
def test_csv_file(db):
    category = Category.objects.create(
        name=fake.word()
    )
    image = SimpleUploadedFile(
        name='test_image.jpg',
        content=open('C:/IT/drinks.jpg', 'rb').read(),
        content_type='image/jpeg'
    )
    with open('test.csv', 'w') as file:
        fieldnames = ['name', 'category', 'description', 'price', 'sku']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({
            'name': fake.name(),
            'category': category.name,
            'description': fake.sentence(),
            'price': fake.pydecimal(
                min_value=1,
                left_digits=DECIMAL_PLACES,
                right_digits=DECIMAL_PLACES,
            ),
            'sku': fake.word(),
        })
    with open('test.csv', 'r') as file:
        yield file
    os.remove(os.getcwd() + '/test.csv')
