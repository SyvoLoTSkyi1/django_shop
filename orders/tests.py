from django.urls import reverse


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


def test_cart_add_or_remove(client, faker, login_user, item):
    url = reverse('cart')
    client, user = login_user

    data = {
        'item': item.id
    }

    fake_data = {
        'item': faker.uuid4()
    }

    response = client.post(reverse('update_cart', args=('add',)), fake_data, follow=True)
    assert response.status_code == 200
    assert not item in response.context_data['order'].items.iterator()

    response = client.post(reverse('update_cart', args=('add',)), data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == url for i in response.redirect_chain)
    assert item in response.context_data['order'].items.iterator()

    response = client.post(reverse('update_cart', args=('remove',)), fake_data, follow=True)
    assert response.status_code == 200
    assert item in response.context_data['order'].items.iterator()

    response = client.post(reverse('update_cart', args=('remove',)), data, follow=True)
    assert response.status_code == 200
    assert not item in response.context_data['order'].items.iterator()
