import pytest
from django.db import IntegrityError, transaction
from django.urls import reverse

from orders.models import OrderItemRelation


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


# def test_cart_add_or_remove(client, faker, login_user, item_factory):
#     url = reverse('cart')
#
#     client, user = login_user
#     response = client.get(url)
#     assert response.status_code == 200
#
#     item = item_factory()
#     data = {
#         'item': item.id
#     }
#
#     fake_data = {
#         'item': faker.uuid4()
#     }
#
#     # response = client.post(reverse('update_cart', args=('add',)), fake_data, follow=True)
#     # assert response.status_code == 200
#     # breakpoint()
#     # assert not item in response.context_data['order'].items.iterator()
#
#     response = client.post(reverse('update_cart', args=('add',)), data, follow=True)
#     assert response.status_code == 200
#     # assert any(i[0] == url for i in response.redirect_chain)
#     response = client.get(url)
#     assert response.status_code == 200
#     breakpoint()
#     assert item in response.context_data['order'].items.iterator()
#
#     response = client.post(reverse('update_cart', args=('remove',)), fake_data, follow=True)
#     assert response.status_code == 200
#     assert item in response.context_data['order'].items.iterator()
#
#     response = client.post(reverse('update_cart', args=('remove',)), data, follow=True)
#     assert response.status_code == 200
#     assert not item in response.context_data['order'].items.iterator()


def test_cart_add_or_remove(client, faker, login_user, order_factory, item_factory, size_factory):
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
    assert not OrderItemRelation.objects.filter(order=order, item=item, size=sizes[0]).exists()

    response = client.post(add_url, data, follow=True)
    assert response.status_code == 200
    assert not OrderItemRelation.objects.filter(order=order, item=item, size=sizes[0]).exists()

    data.update({'size': sizes[0].id})

    response = client.post(add_url, data, follow=True)
    assert response.status_code == 200
    response = client.get(reverse('cart'))
    assert response.status_code == 200
    assert OrderItemRelation.objects.filter(order=order, item=item, size=sizes[0]).exists()
    item_relation = OrderItemRelation.objects.filter(order=order, item=item, size=sizes[0]).first()
    assert item_relation in response.context_data['items_relation']

    remove_url = reverse('update_cart', kwargs={'action': 'remove'})
    response = client.post(remove_url, data, follow=True)
    assert response.status_code == 200
    assert not OrderItemRelation.objects.filter(order=order, item=item, size=sizes[0]).exists()
    assert not response.context_data['items_relation']


def test_cart_clear(client, login_user, order_factory, item_factory, size_factory):
    client, user = login_user

    order = order_factory(user=user)
    item = item_factory()
    size = size_factory()

    order_item_relation = OrderItemRelation.objects.create(
        order=order,
        item=item,
        size=size,
        quantity=1
    )

    response = client.get(reverse('cart'))
    assert response.status_code == 200
    order = response.context_data['order']
    assert OrderItemRelation.objects.filter(order=order, item=item, size=size).exists()
    item_relation = OrderItemRelation.objects.filter(order=order, item=item, size=size).first()
    assert item_relation == order_item_relation
    assert item_relation in response.context_data['items_relation']

    clear_url = reverse('update_cart', kwargs={'action': 'clear'})
    response = client.post(clear_url, follow=True)
    assert response.status_code == 200
    assert not OrderItemRelation.objects.filter(order=order).exists()


def test_order_item_quantity(client, login_user, order_factory, item_factory, size_factory):
    client, user = login_user

    order = order_factory(user=user)
    item = item_factory()
    size = size_factory()

    order_item_relation = OrderItemRelation.objects.create(order=order, item=item, size=size, quantity=3)
    assert order_item_relation.quantity == 3
    assert OrderItemRelation.objects.filter(order=order, item=item, size=size).first().quantity == 3

    order_item_relation.quantity += 2
    order_item_relation.save()
    assert order_item_relation.quantity == 5

    order_item_relation.quantity -= 1
    order_item_relation.save()
    assert order_item_relation.quantity == 4


def test_duplicate_item_with_same_size_in_cart(client, login_user, order_factory, item_factory, size_factory):
    client, user = login_user

    order = order_factory(user=user)
    item = item_factory()
    size = size_factory()

    order_item_relation = OrderItemRelation.objects.create(order=order, item=item, size=size, quantity=1)
    assert order_item_relation.item == item
    assert order_item_relation.size == size

    with pytest.raises(IntegrityError):
        with transaction.atomic():
            OrderItemRelation.objects.create(order=order, item=item, size=size, quantity=1)

    assert OrderItemRelation.objects.filter(order=order, item=item, size=size).count() == 1
