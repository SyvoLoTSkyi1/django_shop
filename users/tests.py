from django.urls import reverse


def test_login_page(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert b'Login' in response.content


def test_sign_up_page(client):
    response = client.get(reverse('sign_up'))
    assert response.status_code == 200
    assert b'Login' in response.content
