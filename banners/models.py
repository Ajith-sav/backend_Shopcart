from django.conf import settings
from django.db import models

# Create your models here.
class Banner(models.Model):
    name = models.CharField(max_length=255)
    image_blob = models.BinaryField()
    staff = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="banner",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
