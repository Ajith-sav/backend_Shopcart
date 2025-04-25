from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_to_email(email, username, otp):
    subject = "Reset Password to ShopCart account."
    html_content = render_to_string("email.html", {"username": username, "otp": otp})

    text_content = strip_tags(html_content)

    email_msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
    )

    email_msg.attach_alternative(html_content, "text/html")

    email_msg.send()
