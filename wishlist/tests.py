from django.urls import reverse

from wishlist.models import WishlistItem


def test_wishlist_page(client, login_user):
    url = reverse('wishlist')

    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'wishlist/items_wishlist.html' for template in response.templates)
    assert b'Wishlist' in response.content


def test_wishlist_list(client, login_user, item_factory, wishlist_item_factory):
    url = reverse('wishlist')

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context_data['object_list']

    item = item_factory()
    wishlist_item = wishlist_item_factory(user=user, item=item)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 1
    assert wishlist_item == response.context_data['object_list'][0]


def test_ajax_update_wishlist(client, faker, login_user, item_factory):
    url = reverse('wishlist')

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context_data['object_list']

    item = item_factory()
    data = {
        'item': item.id
    }

    fake_data = {
        'item': faker.uuid4()
    }

    response = client.get(
        reverse('ajax_update_wishlist', args=(fake_data['item'],)),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    assert response.status_code == 404

    response = client.get(
        reverse('ajax_update_wishlist', args=(data['item'],)),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['created'] is True
    assert WishlistItem.objects.filter(item=item, user=user).exists()

    wishlist_url = reverse('wishlist')
    response = client.get(wishlist_url)
    assert response.status_code == 200
    wishlist_items = response.context['object_list']
    items_in_wishlist = [wishlist_item.item for wishlist_item in wishlist_items]
    assert item in items_in_wishlist

    response = client.get(
        reverse('ajax_update_wishlist', args=(data['item'],)),
        HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    assert response.status_code == 200
    json_response = response.json()
    assert json_response['created'] is False
    assert not WishlistItem.objects.filter(item=item, user=user).exists()

    response = client.get(wishlist_url)
    assert response.status_code == 200
    wishlist_items = response.context['object_list']
    items_in_wishlist = [wishlist_item.item for wishlist_item in wishlist_items]
    assert not item in items_in_wishlist
