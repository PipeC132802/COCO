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
                                     from_email="pipe de COCO <{}>".format(
                                         EMAIL_HOST_USER),
                                     to=email)
        email_message.content_subtype = 'html'
        email_message.send()
        return True
    except:
        return False

"""{
"email":"andrescercal@hotmail.com",
"aim": "change"
}"""
