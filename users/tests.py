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


def test_sign_up_user(client, faker):
    url = reverse('sign_up')
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'registration/sign_up.html' for template in response.templates)

    email = faker.email()
    phone = '+390735119865'
    password = faker.password()
    data = {
        'email': faker.word(),
        'phone': faker.word(),
        'password1': faker.password(),
        'password2': faker.password()
    }

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert 'Enter a valid email address.' in response.content.decode()
    assert 'Enter a valid email address.' in response.context['form'].errors['email']

    data['email'] = email
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert 'Enter a valid phone number (e.g. +12125552368).' in response.content.decode()
    assert 'Enter a valid phone number (e.g. +12125552368).' in response.context['form'].errors['phone']

    data['phone'] = phone
    response = client.post(url, data=data)

    assert response.status_code == 200
    assert "Passwords didn&#x27;t match" in response.content.decode()
    assert "Passwords didn't match" in response.context['form'].errors['__all__']

    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data, follow=True)

    assert response.status_code == 200
    assert email == User.objects.all()[0].email
    assert any(template.name == 'main/index.html' for template in response.templates)



