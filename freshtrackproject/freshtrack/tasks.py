from django_q.tasks import async_task
from django.utils import timezone
from datetime import timedelta
from .models import Product, Notification

def check_expirations():
    today = timezone.now().date()
    expiring_soon = today + timedelta(days=5)

    products_expiring_soon = Product.objects.filter(expiration_date__lte=expiring_soon, expiration_date__gte=today)
    expired_products = Product.objects.filter(expiration_date__lt=today)

    for product in products_expiring_soon:
        message = f'The product {product.name} is expiring soon on {product.expiration_date}.'
        if not Notification.objects.filter(user=product.user, product=product, message=message).exists():
            Notification.objects.create(
                user=product.user,
                product=product,
                message=message
            )

    for product in expired_products:
        message = f'The product {product.name} has expired on {product.expiration_date}.'
        if not Notification.objects.filter(user=product.user, product=product, message=message).exists():
            Notification.objects.create(
                user=product.user,
                product=product,
                message=message
            )