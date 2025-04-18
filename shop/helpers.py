import logging

from django.core.mail import EmailMultiAlternatives
from django.template import loader

logger = logging.getLogger(__name__)


def send_html_mail(subject_template_name, email_template_name, from_email,
                   to_email, context=None, html_email_template_name=None):
    """
    Send a django.core.mail.EmailMultiAlternatives to `to_email`.
    """
    subject = loader.render_to_string(subject_template_name, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name, context)

    email_message = EmailMultiAlternatives(subject, body, from_email,
                                           [to_email])

    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')

    email_message.send()


def send_sms(phone: str, code: int):
    # print(f'Code {code} has sent to number {phone}')
    logger.info(f'Code {code} has sent to number {phone}')
