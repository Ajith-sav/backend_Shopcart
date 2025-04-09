import datetime
import os

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def getFileName(request, filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    new_filename = "%s%s" % (now_time, filename)
    return os.path.join("products/", new_filename)


class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Products(models.Model):

    name = models.CharField(max_length=150, blank=False, null=False)
    brand_name = models.CharField(max_length=150, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=False, null=False)
    image = models.ImageField(
        upload_to=getFileName, null=True, help_text="Image of the product"
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=10, null=False, blank=False
    )
    stock = models.PositiveIntegerField(null=False, blank=False)
    available = models.BooleanField(default=True)
    categories = models.ManyToManyField(
        Category,
        related_name="products",
        blank=False,
    )
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="products",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
