from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .settings import EMAIL_HOST_USER


def sendMail(configs, context):
    email = configs["to"]
    subject = configs["subject"]
    Template = configs["Template"]
    try:
        body = render_to_string(Template, context)
        email_message = EmailMessage(subject=subject,
                                     body=body,
                                     from_email="Felipe (@pipe) de COCO <{}>".format(
                                         EMAIL_HOST_USER),
                                     to=email)
        email_message.content_subtype = 'html'
        email_message.send()
        return True
    except:
        return False


def send_mail_with_file(configs, context):
    email = configs["to"]
    subject = configs["subject"]
    Template = configs["Template"]

    body = render_to_string(Template, context)
    email_message = EmailMessage(subject=subject,
                                 body=body,
                                 from_email="COCO <{}>".format(EMAIL_HOST_USER),
                                 to=email)
    email_message.content_subtype = 'html'
    email_message.send()
