from django.core import mail
from django.urls import reverse


def test_main_page(client):
    response = client.get(reverse('main'))
    assert response.status_code == 200
    assert b'Main' in response.content


def test_contact_us_page(client, faker):
    response = client.get(reverse('contacts'))
    assert response.status_code == 200
    assert b'Contact Us' in response.content

    data = {
        'email': faker.word(),
        'text': faker.sentence()
    }
    response = client.post(reverse('contacts'), data=data)
    assert response.status_code == 200
    assert not len(mail.outbox)

    data = {
        'email': faker.email(),
        'text': faker.sentence()
    }
    response = client.post(reverse('contacts'), data=data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('contacts') for i in response.redirect_chain)
    assert len(mail.outbox) == 1
    assert data['email'] in mail.outbox[0].body
    assert data['text'] in mail.outbox[0].body
