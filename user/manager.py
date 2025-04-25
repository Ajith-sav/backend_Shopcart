from django.contrib.auth.models import BaseUserManager
import pyotp


class CustomUserManager(BaseUserManager):

    def create_user(
        self, email, username, password=None, role="customer", **extra_fields
    ):
        if not email:
            raise ValueError("Please enter valid email")
        email = self.normalize_email(email)
        extra_fields.setdefault("role", role)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("is_staff always have is_staff = True")

        return self.create_user(email, username, password, **extra_fields)


class OTPManager:
    """Helper class to manage OTP operations"""

    @staticmethod
    def generate_otp_secret():
        """Generate a secure random OTP secret"""
        return pyotp.random_base32()

    @staticmethod
    def generate_otp_code(secret):
        """Generate time-based OTP code"""
        totp = pyotp.TOTP(secret, interval=300)  # 5 minutes validity
        return totp.now()

    @staticmethod
    def verify_otp(secret, otp_code):
        """Verify OTP code against secret"""
        totp = pyotp.TOTP(secret, interval=300)
        return totp.verify(otp_code)
