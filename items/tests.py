from django.urls import reverse

from items.models import Item


def test_items_page(client, item):
    response = client.get(reverse('items'))
    assert response.status_code == 200
    assert any(template.name == 'items/item_list.html' for template in response.templates)
    assert b'Items' in response.content
    assert item in response.context_data['object_list']


def test_items_list(login_user, item_factory, faker):
    client, user = login_user
    response = client.get(reverse('items'))
    assert response.status_code == 200
    assert not response.context_data['object_list']

    item = item_factory()
    response = client.get(reverse('items'))
    assert response.status_code == 200
    assert len(response.context_data['object_list']) == 3

    response = client.get(reverse('item_detail', args=(faker.uuid4(),)))
    assert response.status_code == 404

    response = client.get(reverse('item_detail', args=(str(item.id),)))
    assert response.status_code == 200


def test_item_detail_page(client, faker, login_user, item):
    url = reverse('items')
    response = client.get(url + faker.uuid4())
    assert response.status_code == 404

    response = client.get(url + str(item.id))
    assert response.status_code == 200
    assert any(template.name == 'items/item_detail.html' for template in response.templates)
    assert item.name.encode() in response.content

    client, user = login_user
    response = client.get(url + str(item.id))
    assert response.status_code == 200
    assert item.name.encode() in response.content


def test_export_csv(client, item, login_user):
    url = reverse('export_csv')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)
    assert any(template.name == 'registration/login.html' for template in response.templates)

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
    assert any(template.name == 'registration/login.html' for template in
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
