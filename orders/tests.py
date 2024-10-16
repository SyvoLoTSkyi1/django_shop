import pytest
from _decimal import Decimal
from django.db import IntegrityError, transaction
from django.urls import reverse

from orders.models import OrderItemRelation, Order
from shop.model_choices import DiscountTypes


def test_cart_page(client, faker, login_user):
    url = reverse('cart')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'orders/cart.html' for template in response.templates)
    assert b'Cart' in response.content
    assert user == response.context['order'].user


def test_cart_add_or_remove(client, faker, login_user,
                            order_factory, item_factory,
                            size_factory):

    client, user = login_user

    order = order_factory(user=user)
    sizes = [size_factory(), size_factory()]
    item = item_factory(size=sizes)

    fake_data = {
        'item': faker.uuid4(),
        'size': sizes[0].id
    }
    data = {
        'item': item.id,
    }
    add_url = reverse('update_cart', kwargs={'action': 'add'})
    response = client.post(add_url, fake_data, follow=True)
    assert response.status_code == 200
    assert not OrderItemRelation.objects.filter(
        order=order, item=item, size=sizes[0])\
        .exists()

    response = client.post(add_url, data, follow=True)
    assert response.status_code == 200
    assert not OrderItemRelation.objects.filter(
        order=order, item=item, size=sizes[0])\
        .exists()

    data.update({'size': sizes[0].id})

    response = client.post(add_url, data, follow=True)
    assert response.status_code == 200
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert OrderItemRelation.objects.filter(
        order=order, item=item, size=sizes[0])\
        .exists()
    item_relation = OrderItemRelation.objects.filter(
        order=order, item=item, size=sizes[0])\
        .first()
    assert item_relation in response.context_data['items_relation']

    remove_url = reverse('update_cart', kwargs={'action': 'remove'})
    response = client.post(remove_url, data, follow=True)
    assert response.status_code == 200
    assert not OrderItemRelation.objects.filter(
        order=order, item=item, size=sizes[0])\
        .exists()
    assert not response.context_data['items_relation']


def test_cart_clear(client, login_user,
                    order_factory, item_factory,
                    size_factory):

    client, user = login_user

    order = order_factory(user=user)
    item = item_factory()
    size = size_factory()

    order_item_relation = OrderItemRelation.objects.create(
        order=order, item=item,
        size=size, quantity=1)

    response = client.get(reverse('cart'))
    assert response.status_code == 200
    order = response.context_data['order']
    assert OrderItemRelation.objects.filter(
        order=order, item=item, size=size)\
        .exists()
    item_relation = OrderItemRelation.objects.filter(
        order=order, item=item, size=size)\
        .first()
    assert item_relation == order_item_relation
    assert item_relation in response.context_data['items_relation']

    clear_url = reverse('update_cart', kwargs={'action': 'clear'})
    response = client.post(clear_url, follow=True)
    assert response.status_code == 200
    assert not OrderItemRelation.objects.filter(order=order).exists()


def test_order_item_quantity(client, login_user,
                             order_factory, item_factory,
                             size_factory):
    client, user = login_user

    order = order_factory(user=user)
    item = item_factory()
    size = size_factory()

    order_item_relation = OrderItemRelation.objects.create(
        order=order, item=item,
        size=size, quantity=3)
    assert order_item_relation.quantity == 3
    assert OrderItemRelation.objects.filter(
        order=order, item=item,
        size=size).first()\
        .quantity == 3

    order_item_relation.quantity += 2
    order_item_relation.save()
    assert order_item_relation.quantity == 5

    order_item_relation.quantity -= 1
    order_item_relation.save()
    assert order_item_relation.quantity == 4


def test_duplicate_item_with_same_size_in_cart(client, login_user,
                                               order_factory, item_factory,
                                               size_factory):

    client, user = login_user

    order = order_factory(user=user)
    item = item_factory()
    size = size_factory()

    order_item_relation = OrderItemRelation.objects.create(
        order=order, item=item,
        size=size, quantity=1)
    assert order_item_relation.item == item
    assert order_item_relation.size == size

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            OrderItemRelation.objects.create(
                order=order, item=item,
                size=size, quantity=1)

    assert OrderItemRelation.objects.filter(
        order=order, item=item,
        size=size)\
        .count() == 1


def test_cart_confirm_page(client, faker, login_user, order_factory):
    url = reverse('confirm_cart')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    order_factory(user=user)
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'orders/cart_confirm.html' for template in response.templates)
    assert user == response.context['order'].user


def test_cart_confirm_page_form(client, faker, login_user, order_factory):
    client, user = login_user
    order_factory(user=user)
    response = client.get(reverse('confirm_cart'))
    assert response.status_code == 200
    assert 'form' in response.context
    assert 'first_name' in response.context['form'].fields
    assert 'last_name' in response.context['form'].fields
    assert 'email' in response.context['form'].fields
    assert 'phone' in response.context['form'].fields
    assert 'country' in response.context['form'].fields
    assert 'city' in response.context['form'].fields
    assert 'address' in response.context['form'].fields
    assert b'<form' in response.content


def test_cart_pay(client, faker, login_user,
                  order_factory, item_factory,
                  size_factory):

    client, user = login_user

    order = order_factory(user=user)
    item = item_factory()
    size = size_factory()

    OrderItemRelation.objects.create(
        order=order, item=item,
        size=size, quantity=1)

    response = client.get(reverse('confirm_cart'))
    assert response.status_code == 200
    assert response.context_data['order']

    pay_url = reverse('update_cart', kwargs={'action': 'pay'})
    response = client.post(pay_url, follow=True)
    assert response.status_code == 200
    order = Order.objects.filter(user=user).first()
    assert not order.is_active
    assert order.is_paid


def test_apply_discount_to_order(client, faker, login_user,
                                 user_factory, order_factory,
                                 item_factory, size_factory,
                                 discount_factory):

    user = user_factory()
    discount_value = discount_factory(
        amount=Decimal('10.00'),
        discount_type=DiscountTypes.VALUE
    )
    discount_percent = discount_factory(
        amount=Decimal('10.00'),
        discount_type=DiscountTypes.PERCENT
    )

    order = order_factory(user=user)

    item = item_factory(actual_price=Decimal('100.00'))
    size = size_factory()
    OrderItemRelation.objects.create(
        order=order, item=item,
        size=size, quantity=1)

    total_amount_before_discount = order.get_total_amount()
    assert total_amount_before_discount == Decimal('100.00')

    order.discount = discount_value
    order.save()

    order_after_discount_value = order.get_total_amount()
    assert order_after_discount_value == Decimal('90.00')

    order.discount = discount_percent
    order.save()

    order_after_discount_percent = order.get_total_amount()
    assert order_after_discount_percent == Decimal('90.00')


def test_recalculate_cart_total_amount(client, faker, login_user,
                                       order_factory, item_factory,
                                       size_factory):

    client, user = login_user

    order = order_factory(user=user)
    item = item_factory(actual_price=Decimal('50.00'))
    size = size_factory()

    item_relation = OrderItemRelation.objects.create(
        order=order, item=item,
        size=size, quantity=1)

    assert item_relation.quantity == 1
    assert order.get_total_amount() == Decimal('50.00')

    fake_item_relation_pk = faker.uuid4()
    fake_form_data = {
        f'item_{fake_item_relation_pk}': str(faker.uuid4()),
        f'size_{fake_item_relation_pk}': str(faker.uuid4()),
        f'quantity_{fake_item_relation_pk}': 3
    }
    form_data = {
        f'item_{item_relation.pk}': str(item.pk),
        f'size_{item_relation.pk}': str(size.pk),
        f'quantity_{item_relation.pk}': 3
    }

    response = client.post(reverse('recalculate_cart'), data=fake_form_data)
    assert response.status_code == 302
    assert response.url == reverse('cart')
    item_relation.refresh_from_db()
    assert item_relation.quantity != 3

    response = client.post(reverse('recalculate_cart'), data=form_data)

    assert response.status_code == 302
    assert response.url == reverse('cart')

    item_relation.refresh_from_db()
    assert item_relation.quantity == 3
    order.refresh_from_db()
    assert order.get_total_amount() == Decimal('150.00')


def test_success_cart_confirm_page(client, faker, login_user):
    url = reverse('success_confirm_cart')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'orders/cart_confirm_success.html' for template in response.templates)