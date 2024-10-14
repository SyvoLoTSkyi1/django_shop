import csv
import os

import factory
import pprintpp
import pytest
from _decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from faker import Faker
from django.test.client import Client
from pytest_factoryboy import register

from items.models import Category, Item, PopularItem, Size
from orders.models import Order, Discount
from shop.constants import DECIMAL_PLACES
from shop.model_choices import Currency, DiscountTypes
from wishlist.models import WishlistItem

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


# @pytest.fixture(scope='function')
# def item(db):
#     category = Category.objects.create(
#         name='guygiuyguy'
#     )
#
#     image = SimpleUploadedFile(
#         name='test_image.jpg',
#         content=open('C:/IT/drinks.jpg', 'rb').read(),
#         content_type='image/jpeg'
#     )
#
#     item = Item.objects.create(
#         name=fake.word(),
#         category=category,
#         image=image
#     )
#     yield item


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    print("DB access enabled for all tests")
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
class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda x: str(fake.random_int(min=35, max=50)))


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda x: fake.email())
    first_name = factory.Sequence(lambda x: fake.first_name())
    last_name = factory.Sequence(lambda x: fake.last_name())
    phone = factory.Sequence(lambda x: fake.phone_number())
    is_phone_valid = False
    is_email_valid = False
    is_staff = False
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)


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
    actual_price = factory.Sequence(lambda x: fake.pydecimal(
        min_value=1,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES
    ))
    currency = factory.LazyFunction(lambda: fake.random_element(Currency.choices)[0])
    sku = factory.Sequence(lambda x: fake.word())
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def size(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for size in extracted:
                self.size.add(size)

    # @factory.post_generation
    # def post_create(self, created, *args, **kwargs):
    #     if created and not kwargs.get('deny_post'):
    #         for _ in range(1, 3):
    #             self.items.add(ItemFactory(post_create__deny_post=True))


@register
class PopularItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PopularItem
        django_get_or_create = ('item',)

    item = factory.SubFactory(ItemFactory)


@register
class WishlistItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WishlistItem

    user = factory.SubFactory(UserFactory)
    item = factory.SubFactory(ItemFactory)


@register
class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount

    amount = factory.Sequence(lambda x: fake.pydecimal(
        min_value=1,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES
    ))
    code = factory.Faker('lexify', text='??????')
    is_active = True
    discount_type = factory.LazyFunction(lambda: DiscountTypes.VALUE if factory.Faker('boolean') else DiscountTypes.PERCENT)


@register
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    discount = factory.SubFactory(DiscountFactory)

    total_amount = factory.LazyFunction(lambda: Decimal('0.00'))
    is_active = True
    is_paid = False

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for item in extracted:
                self.items.add(item)


@pytest.fixture(scope='function')
def login_user(db):
    password = '123456789'
    # user, _ = User.objects.get_or_create(
    #     email=email,
    #     first_name='John',
    #     phone=phone,
    #     is_phone_valid=True
    # )
    user = UserFactory(is_email_valid=True)
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'),
                           data={'username': user.email,
                                 'password': password}
                           )

    assert response.status_code == 302
    yield client, user


@pytest.fixture(scope='function')
def login_user_is_staff(db):
    password = '123456789'
    # user, _ = User.objects.get_or_create(
    #     email=email,
    #     first_name='John',
    #     phone=phone,
    #     is_phone_valid=True
    # )
    user = UserFactory(is_email_valid=True, is_staff=True)
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('login'),
                           data={'username': user.email,
                                 'password': password}
                           )

    assert response.status_code == 302
    yield client, user


@pytest.fixture(scope='function')
def test_csv_file(db):
    category = Category.objects.create(
        name=fake.word()
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
