import logging
import random

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from shop import settings
from shop.celery import app
from shop.helpers import send_html_mail, send_sms


User = get_user_model()
logger = logging.getLogger(__name__)


@app.task
def send_mail_checker(subject_template_name, email_template_name, from_email,
                      to_email, context=None, html_email_template_name=None):
    send_html_mail(
        subject_template_name,
        email_template_name,
        from_email,
        to_email,
        context,
        html_email_template_name
    )


@app.task
def send_verification_sms(user_id, phone):
    """
    Generates a code, saves it in the cache and sends an SMS.
    """
    try:
        user = User.objects.get(id=user_id)  # noqa
    except User.DoesNotExist:
        logger.warning(f"User with ID {user_id} does not exist.")
        return

    code = random.randint(10000, 99999)
    cache.set(f'{str(user_id)}_code', code, timeout=60)
    send_sms(phone, code)


@app.task
def send_confirmation_email(user_id):
    """
    Sends an email to confirm the user's email.
    """

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.warning(f"User with ID {user_id} does not exist.")
        return

    context = {
        'email': user.email,
        'domain': settings.DOMAIN,
        'site_name': 'SHOP',
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'user': user,
        'token': default_token_generator.make_token(user),
        'subject': 'Confirm email',
        'is_registration': not user.is_active
    }
    subject_template_name = 'users/registration/confirm_subject.txt'  # noqa
    email_template_name = 'users/registration/confirm_email_text.html'  # noqa
    send_html_mail(
        subject_template_name,
        email_template_name,
        from_email=settings.SERVER_EMAIL,
        to_email=user.email,
        context=context
    )
