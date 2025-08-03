from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from modules.orders.models import OrderItem


@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
        else:
            product.stock = 0
        product.available = product.stock > 0
        product.save()


@receiver(post_delete, sender=OrderItem)
def restore_stock(sender, instance, **kwargs):
    product = instance.product
    product.stock += instance.quantity
    product.available = product.stock > 0
    product.save()
