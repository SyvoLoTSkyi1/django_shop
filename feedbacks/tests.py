from django.urls import reverse

from feedbacks.models import Feedback


def test_feedbacks(client, faker, login_user):
    url = reverse('feedbacks')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('login') + f'?next={url}' for i in response.redirect_chain)

    client, user = login_user
    response = client.get(url)
    assert response.status_code == 200
    assert b'Please, leave your feedback' in response.content

    assert not Feedback.objects.exists()

    data = {
        'user': str(user.id),
        'text': faker.text(),
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['rating'][0] == 'This field is required.'

    assert not Feedback.objects.exists()

    data = {
        'user': str(user.id),
        'rating': 3,
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['text'][0] == 'This field is required.'

    assert not Feedback.objects.exists()

    data = {
        'text': faker.text(),
        'rating': 3,
        'user': str(user.id)
    }

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert Feedback.objects.exists()
