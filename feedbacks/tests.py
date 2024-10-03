from django.urls import reverse

from feedbacks.models import Feedback


def test_feedbacks_page(client, login_user):
    url = reverse('feedbacks')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert b'Please, leave your feedback' in response.content


def test_feedbacks_list(client, faker, login_user):
    url = reverse('feedbacks')

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert not Feedback.objects.exists()

    data = {
        'user': user.id,
        'text': faker.text(),
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['rating'][0] == 'This field is required.'
    assert not Feedback.objects.exists()

    data = {
        'user': user.id,
        'rating': 3,
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['text'][0] == 'This field is required.'
    assert not Feedback.objects.exists()

    data = {
        'text': faker.text(),
        'rating': 3,
        'user': user.id
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert Feedback.objects.exists()


def test_feedback(client, faker, login_user):
    url = reverse('feedbacks')

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert not Feedback.objects.exists()

    data = {
        'text': faker.text(),
        'rating': 3,
        'user': user.id
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert Feedback.objects.exists()
    feedback = Feedback.objects.first()
    assert feedback is not None
    assert feedback.user == user
    assert feedback.text == data['text']
    assert feedback.rating == data['rating']
