from django.urls import reverse

from items.filters import ItemFilter
from items.models import Item


def test_items_page(client, item_factory):
    response = client.get(reverse('items'))
    assert response.status_code == 200
    assert any(template.name == 'items/item_list.html' for template in response.templates)
    assert b'Items' in response.content

    items = item_factory()
    response = client.get(reverse('items'))
    assert response.status_code == 200
    assert items in response.context_data['object_list']
    assert 'wishlist_items' in response.context_data
    assert not response.context_data['wishlist_items']
    assert 'query_params' in response.context_data
    assert not response.context_data['query_params']


def test_items_page_pagination_and_filters(client, item_factory):
    url = reverse('items')
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context_data['object_list']

    items = item_factory.create_batch(1)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context_data['items']) == 1
    assert len(response.context_data['object_list']) == 1
    assert response.context_data['is_paginated'] is False

    items.extend(item_factory.create_batch(6))
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context_data['items']) == 7
    assert len(response.context_data['object_list']) == 6
    assert response.context_data['is_paginated'] is True

    assert 'filter' in response.context_data
    filter_instance = response.context_data['filter']
    assert isinstance(filter_instance, ItemFilter)

    filter_params = {'name': items[0].name}
    response = client.get(url, data=filter_params)
    assert response.status_code == 200
    filtered_items = response.context_data['item_list']
    assert filtered_items == response.context_data['object_list']
    assert len(filtered_items) == 1
    assert filtered_items[0] == items[0]


def test_items_list(login_user, item_factory, wishlist_item_factory, faker):
    url = reverse('items')
    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context_data['object_list']

    item = item_factory()
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 1
    assert not response.context_data['wishlist_items']

    wishlist_item_factory(user=user, item=item)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context_data['wishlist_items']) == 1
    assert item.id in response.context_data['wishlist_items']

    response = client.get(reverse('item_detail', args=(faker.uuid4(),)))
    assert response.status_code == 404

    response = client.get(reverse('item_detail', args=(str(item.id),)))
    assert response.status_code == 200


def test_item_detail_page(client, faker, login_user, item_factory, size_factory):
    url = reverse('items')
    response = client.get(url + faker.uuid4())
    assert response.status_code == 404

    item = item_factory(size=[size_factory(), size_factory()])
    response = client.get(url + str(item.id))
    assert response.status_code == 200
    assert any(template.name == 'items/item_detail.html' for template in response.templates)
    assert item.name.encode() in response.content

    for size in item.size.all():
        assert size.name.encode() in response.content

    client, user = login_user
    response = client.get(url + str(item.id))
    assert response.status_code == 200
    assert item.name.encode() in response.content

    for size in item.size.all():
        assert size.name.encode() in response.content


def test_popular_items_page(client, popular_item_factory):
    response = client.get(reverse('popular_items'))
    assert response.status_code == 200
    assert any(template.name == 'items/popular_items.html' for template in response.templates)
    assert b'Popular' in response.content

    popular_items = popular_item_factory()
    response = client.get(reverse('popular_items'))
    assert response.status_code == 200
    assert popular_items in response.context_data['object_list']
    assert 'wishlist_items' in response.context_data
    assert not response.context_data['wishlist_items']
    assert 'query_params' in response.context_data
    assert not response.context_data['query_params']


def test_export_csv(client, login_user):

    url = reverse('export_csv')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)
    assert any(template.name == 'users/registration/login.html' for template in response.templates)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert 'filename="items.csv"' in response.headers['Content-Disposition']
    assert all(item.name.encode() in response.content for item in Item.objects.iterator())


def test_import_csv(client, login_user_is_staff, login_user, test_csv_file):
    url = reverse('import_csv')

    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in
               response.redirect_chain)
    assert any(template.name == 'users/registration/login.html' for template in
               response.templates)

    client, user = login_user
    response = client.get(url)

    assert user.is_staff == False
    assert response.status_code == 403

    client, user = login_user_is_staff
    response = client.get(url)
    assert response.status_code == 200
    assert b'Import CSV' in response.content

    response = client.post(url, data={'csv_file': test_csv_file}, follow=True)
    assert response.status_code == 200
    assert len(response.context['object_list']) == 1


def test_item_search(client, item_factory):
    response = client.get(reverse('item_search'))
    assert response.status_code == 200
    assert any(template.name == 'items/item_list.html' for template in response.templates)

    items = item_factory.create_batch(3)
    response = client.get(reverse('item_search'))
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 3
    assert 'query_params' in response.context_data
    assert not response.context_data['query_params']

    query_params = {'query': items[0].name}
    response = client.get(reverse('item_search'), data=query_params)
    assert response.status_code == 200
    searched_items = response.context_data['item_list']
    assert searched_items == response.context_data['object_list']
    assert len(searched_items) == 1
    assert searched_items[0] == items[0]
