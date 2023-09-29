from django.urls import reverse


def test_items_page(client):
    response = client.get(reverse('items'))
    assert response.status_code == 200
    assert any(template.name == 'items/item_list.html' for template in response.templates)
    assert b'Items' in response.content
    # assert item in response.context_data['object_list']
