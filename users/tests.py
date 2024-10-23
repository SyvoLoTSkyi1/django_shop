import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse

User = get_user_model()


def test_login_user_with_email(client, faker, user_factory):
    url = reverse('login')
    user = user_factory(is_email_valid=True)
    password = '123456789'
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

    assert response.context['form'].errors['__all__'][0] == 'Email or phone number is required'

    data['username'] = faker.email()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Please enter a correct email address and password. Note that both fields may be case-sensitive.'

    data['username'] = user.email
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 302


def test_login_user_with_phone(client, faker, user_factory):
    url = reverse('login')
    user = user_factory(is_phone_valid=True)
    password = '123456789'
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

    assert response.context['form'].errors['__all__'][0] == 'Email or phone number is required'

    data['phone'] = faker.phone_number()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Please enter a correct email address and password. Note that both fields may be case-sensitive.'

    data['phone'] = user.phone
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 302


def test_sign_up_user(client, faker):
    # url = reverse('sign_up')
    # response = client.get(url)
    # assert response.status_code == 200
    # assert any(template.name == 'registration/sign_up.html' for template in response.templates)
    #
    # email = faker.email()
    # phone = '+390735119865'
    # password = faker.password()
    # assert not User.objects.filter(email=email).exists()
    # assert len(mail.outbox) == 0
    # data = {
    #     'email': faker.word(),
    #     'phone': faker.word(),
    #     'password1': faker.password(),
    #     'password2': faker.password()
    # }
    #
    # response = client.post(url, data=data)
    # assert response.status_code == 200
    # assert 'Enter a valid email address.' in response.content.decode()
    # assert 'Enter a valid email address.' in response.context['form'].errors['email']
    # assert len(mail.outbox) == 0
    #
    # data['email'] = email
    # response = client.post(url, data=data)
    # assert response.status_code == 200
    # assert 'Enter a valid phone number (e.g. +12125552368).' in response.content.decode()
    # assert 'Enter a valid phone number (e.g. +12125552368).' in response.context['form'].errors['phone']
    # assert len(mail.outbox) == 0
    #
    # data['phone'] = phone
    # response = client.post(url, data=data)
    #
    # assert response.status_code == 200
    # assert "Passwords didn&#x27;t match" in response.content.decode()
    # assert "Passwords didn't match" in response.context['form'].errors['__all__']
    # assert len(mail.outbox) == 0
    #
    # data['password1'] = password
    # data['password2'] = password
    # response = client.post(url, data=data, follow=True)
    #
    # # assert response.status_code == 200
    # # assert email == User.objects.all()[0].email
    # # assert any(template.name == 'main/index.html' for template in response.templates)
    # assert response.status_code == 200
    # assert User.objects.filter(email=email, is_active=False).exists()
    #
    # assert len(mail.outbox) == 1
    # uidb64, token = re.search("sign_up/(.*)/(.*)/confirm", mail.outbox[0].body).groups()
    # response = client.get(reverse('sign_up_confirm', args=(uidb64, token)))
    # assert response.status_code == 302
    #
    # assert User.objects.filter(email=email, is_active=True).exists()
    email = faker.email()
    password = faker.password()
    url = reverse('sign_up')
    assert not User.objects.filter(email=email).exists()
    assert len(mail.outbox) == 0
    data = {
        'password1': password,
        'password2': password,
        'email': email
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert User.objects.filter(email=email, is_active=False).exists()
    assert len(mail.outbox) == 1

    response = client.post(reverse('login'), data={'email': email, 'password': password})
    assert response.status_code == 200

    uidb64, token = re.search("sign_up/(.*)/(.*)/confirm", mail.outbox[0].body).groups()
    response = client.get(reverse('sign_up_confirm', args=(uidb64, token)))
    assert response.status_code == 302

    assert User.objects.filter(email=email, is_active=True).exists()

    response = client.post(reverse('login'), data={'username': email, 'password': password})
    assert response.status_code == 302