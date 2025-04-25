from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags

from .models import *


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


class OTPService:
    """Service layer for OTP operations"""

    @staticmethod
    def create_or_update_otp(user):
        """Create or update OTP record for user"""
        secret = OTPManager.generate_otp_secret()
        otp, created = OTP.objects.update_or_create(
            user=user,
            defaults={
                "otp_secret": secret,
                "is_verified": False,
                "created_at": timezone.now(),
            },
        )
        return otp

    @staticmethod
    def get_valid_otp_record(user, otp_code=None):
        """Get valid unexpired OTP record"""
        time_threshold = timezone.now() - timedelta(minutes=5)
        queryset = OTP.objects.filter(
            user=user, created_at__gte=time_threshold, is_verified=False
        )

        if otp_code:
            queryset = queryset.filter(otp_secret=otp_code)

        return queryset.order_by("-created_at").first()
