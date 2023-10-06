from django.urls import reverse


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
    assert user == response.context['wishlist'].user


def test_wishlist_add_and_remove(client, faker, login_user, item):
    url = reverse('wishlist')
    client, user = login_user

    data = {
        'item': item.id
    }

    fake_data = {
        'item': faker.uuid4()
    }

    response = client.post(reverse('update_wishlist', args=('add',)), fake_data, follow=True)
    assert response.status_code == 200
    assert not item in response.context_data['wishlist'].items.iterator()

    response = client.post(reverse('update_wishlist', args=('add',)), data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == url for i in response.redirect_chain)
    assert item in response.context_data['wishlist'].items.iterator()

    response = client.post(reverse('update_wishlist', args=('remove',)), fake_data, follow=True)
    assert response.status_code == 200
    assert item in response.context_data['wishlist'].items.iterator()

    response = client.post(reverse('update_wishlist', args=('remove',)), data, follow=True)
    assert response.status_code == 200
    assert not item in response.context_data['wishlist'].items.iterator()

