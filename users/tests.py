from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


def test_login_user(client, faker):
    email = faker.email()
    password = faker.password()
    url = reverse('login')
    user = User.objects.create(
        email=email,
        first_name=faker.first_name()
    )
    user.set_password(password)
    user.save()
    # get login page
    response = client.get(url)
    assert response.status_code == 200

    data = {
        'password': faker.password()
    }
    # post data to login form
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['username'][0] == 'This field is required.'

    data['username'] = faker.email()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Please enter a correct email address and password. Note that both fields may be case-sensitive.'

    data['username'] = email
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 302


def test_sign_up_page(client):
    response = client.get(reverse('sign_up'))
    assert response.status_code == 200
    assert b'Login' in response.content
