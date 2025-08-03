from django.conf import settings
from django.db import models

from modules.products.models import Products


class Order(models.Model):
    PAYMENT_STATUS_CHOICE = [
        ("pending", "Pending"),
        ("complete", "Complete"),
        ("failed", "Failed"),
    ]
    placed_at = models.DateTimeField(auto_now_add=True, db_index=True)
    payment_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICE, default="pending", db_index=True
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        db_table = "orders"

    @property
    def total_price(self):
        return sum(item.price * item.quantity for item in self.item.all())

    def update_payment_status(self, status):
        if status in dict(self.PAYMENT_STATUS_CHOICE).keys():
            self.payment_status = status
            self.save()
        else:
            raise ValueError("Invalid payment status")


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="item")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "order_items"

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if self.price <= 0:
            raise ValueError("Price must be greater than zero.")
        super().save(*args, **kwargs)
