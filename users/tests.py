from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


def test_login_user_with_email(client, faker, user_factory):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'users/registration/login.html' for template in response.templates)

    user = user_factory(is_email_valid=True)
    password = '123456789'
    user.set_password(password)
    user.save()

    response = client.get(url)
    assert response.status_code == 200

    data = {
        'password': faker.password()
    }

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
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'users/registration/login.html' for template in response.templates)

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


# def test_sign_up_user_with_email(client, faker, mocker):
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


def test_sign_up_user_with_email(client, faker, mocker):
    url = reverse('sign_up')
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'users/registration/sign_up.html' for template in response.templates)
    mock_send_email = mocker.patch('users.model_forms.send_confirmation_email')

    password = faker.password()
    data = {
        'email': faker.email(),
        'password1': password,
        'password2': password,
    }

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('activation_email')
    user = User.objects.get(email=data['email'], is_active=False, is_email_valid=False)
    assert user is not None

    mock_send_email.assert_called_once_with(user)

    response = client.post(reverse('login'), data={'email': data['email'], 'password': password})
    assert response.status_code == 200
    mock_send_email.stop()

    # uidb64, token = re.search("sign_up/(.*)/(.*)/confirm", mail.outbox[0].body).groups()
    # response = client.get(reverse('sign_up_confirm', args=(uidb64, token)))
    # assert response.status_code == 302
    #
    # assert User.objects.filter(email=email, is_active=True).exists()
    #
    # response = client.post(reverse('login'), data={'username': email, 'password': password})
    # assert response.status_code == 302


def test_signup_user_with_phone(client, faker, mocker):
    url = reverse('sign_up')
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'users/registration/sign_up.html' for template in response.templates)
    mock_send_sms = mocker.patch('users.model_forms.send_verification_sms')

    url = reverse('sign_up')
    password = faker.password()
    data = {
        'phone': '+380660397882',
        'password1': password,
        'password2': password,
    }

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == reverse('confirm_phone')
    user = User.objects.get(phone=data['phone'], is_active=False, is_phone_valid=False)
    assert user is not None

    mock_send_sms.assert_called_once_with(user, data['phone'])

    response = client.post(reverse('login'), data={'email': data['phone'], 'password': password})
    assert response.status_code == 200
    mock_send_sms.stop()


def test_signup_form_invalid(client, faker):
    url = reverse('sign_up')

    password = faker.password()
    data = {
        'password1': password,
        'password2': password,
    }

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Email or phone number is required'

    assert not User.objects.exists()

    data.update({'email': faker.email()})
    data['password2'] = faker.password()

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Enter correct password'

    assert not User.objects.exists()


def test_confirm_email(client, user_factory):
    user = user_factory(is_active=False, is_email_valid=False)
    user.save()

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    url = reverse('confirm_email', kwargs={'uidb64': uid, 'token': token})

    response = client.get(url)
    assert response.status_code == 302
    assert User.objects.filter(is_active=True, is_email_valid=True).exists()


# def test_confirm_phone(client, user_factory, mocker):
#     user = user_factory(is_active=False, is_phone_valid=False)
#     # user.save()
#
#     session = client.session
#     session.clear()
#     session['user_id'] = user.id
#     session.save()
#
#     verification_code = 12345
#     mock_cache = mocker.patch('django.core.cache.cache')
#     mock_cache.get.return_value = verification_code
#
#     # mock_cache_set = mocker.patch('django.core.cache.cache.set')
#     # mock_cache_get = mocker.patch('django.core.cache.cache.get', return_value=verification_code)
#     mock_cache.reset_mock()
#     url = reverse('confirm_phone')
#     response = client.post(url, data={'code': 54321})
#
#     assert response.status_code == 200
#     assert not User.objects.filter(is_active=True, is_phone_valid=True).exists()
#     assert mock_cache.get.called_once_with(f'{user.id}_code')
#     mock_cache.reset_mock()
#
#     response = client.post(url, data={'code': verification_code})
#
#     assert response.status_code == 302
#     assert response.url == reverse('login')
#
#     assert User.objects.filter(is_active=True, is_phone_valid=True).exists()
#     assert mock_cache.get.called_once_with(f'{user.id}_code')
#     mock_cache.stop()
#
#     # user.refresh_from_db()
#     # assert user.is_active is True
#     # assert user.is_phone_valid is True


def test_user_profile_page(client, login_user):
    url = reverse('user_profile')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'users/user_profile.html' for template in response.templates)

    assert response.context_data['user_profile'] == user


def test_user_profile_update(client, login_user, faker):
    url = reverse('user_profile_update')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'users/user_profile_update.html' for template in response.templates)
    # user = user_factory(is_active=False, is_phone_valid=False)
    # user.save()
    # client.force_login(user)

    form_data = {
        'first_name': faker.first_name(),
        'last_name': faker.last_name(),
        'country': faker.country(),
        'city': faker.city(),
        'address': faker.address(),
    }
    response = client.post(url, data=form_data)
    assert response.status_code == 302
    assert User.objects.filter(first_name=form_data['first_name'], last_name=form_data['last_name']).exists()
    # user.refresh_from_db()
    # assert user.first_name == form_data['first_name']
    # assert user.last_name == form_data['last_name']


def test_user_orders(client, login_user, user_factory, order_factory):
    url = reverse('user_orders')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'users/user_orders.html' for template in response.templates)

    order1 = order_factory(user=user)
    order2 = order_factory(user=user, is_active=False, is_paid=True)

    other_user = user_factory()
    other_order = order_factory(user=other_user)

    response = client.get(url)
    assert response.status_code == 200

    orders = response.context['orders']
    assert orders.count() == 2
    assert order1 in orders
    assert order2 in orders
    assert other_order not in orders

    assert response.context['order_count'] == 2
