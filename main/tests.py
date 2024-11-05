from django.core import mail
from django.urls import reverse


def test_main_page(client):
    response = client.get(reverse('main'))
    assert response.status_code == 200
    assert any(template.name == 'main/index.html' for template in response.templates)


# def test_contact_us_page(client, faker):
#     response = client.get(reverse('contacts'))
#     assert response.status_code == 200
#     assert b'Contact Us' in response.content
#
#     data = {
#         'email': faker.word(),
#         'text': faker.sentence()
#     }
#     response = client.post(reverse('contacts'), data=data)
#     assert response.status_code == 200
#     assert not len(mail.outbox)
#
#     data = {
#         'email': faker.email(),
#         'text': faker.sentence()
#     }
#     response = client.post(reverse('contacts'), data=data, follow=True)
#     assert response.status_code == 200
#     assert any(i[0] == reverse('contacts') for i in response.redirect_chain)
#     assert len(mail.outbox) == 1
#     assert data['email'] in mail.outbox[0].body
#     assert data['text'] in mail.outbox[0].body


def test_contact_us_page(client, faker, mocker):
    url = reverse('contacts')
    response = client.get(url)
    assert response.status_code == 200
    assert any(template.name == 'main/contact.html' for template in response.templates)

    mock_send_contact_form = mocker.patch('main.views.send_contact_form')

    invalid_data = {
        'email': faker.word(),
        'text': faker.text()
    }
    response = client.post(url, data=invalid_data)
    assert response.status_code == 200

    data = {
        'email': faker.email(),
        'text': faker.text()
    }

    response = client.post(url, data=data)
    assert response.status_code == 302
    assert response.url == url

    mock_send_contact_form.assert_called_once_with(
        data['email'], data['text']
    )
