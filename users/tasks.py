from shop.celery import app
from shop.helpers import send_html_mail


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
def send_sms(phone: str, code: str):
    print('Code ' + code + ' has sent to number ' + phone)
