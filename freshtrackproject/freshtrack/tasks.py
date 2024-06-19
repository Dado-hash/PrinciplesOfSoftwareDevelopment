from django.utils import timezone
from datetime import timedelta
from .models import Product, Notification
import logging

logger = logging.getLogger(__name__)

def check_expirations():
    logger.debug('Starting check_expirations task.')
    today = timezone.now().date()
    expiring_soon = today + timedelta(days=5)

    products_expiring_soon = Product.objects.filter(expiration_date__lte=expiring_soon, expiration_date__gte=today)
    expired_products = Product.objects.filter(expiration_date__lt=today)

    for product in products_expiring_soon:
        message = f'The product {product.name} is expiring soon on {product.expiration_date}.'
        
        # Elimina le notifiche esistenti per il prodotto con la data di scadenza aggiornata
        Notification.objects.filter(user=product.user, product=product, message=message).delete()
        
        # Crea una nuova notifica per il prodotto con la data di scadenza aggiornata
        Notification.objects.create(
            user=product.user,
            product=product,
            message=message
        )

    for product in expired_products:
        message = f'The product {product.name} has expired on {product.expiration_date}.'
        
        # Elimina le notifiche esistenti per il prodotto con la data di scadenza aggiornata
        Notification.objects.filter(user=product.user, product_id=product.id, message=message).delete()
        
        # Crea una nuova notifica per il prodotto con la data di scadenza aggiornata
        Notification.objects.create(
            user=product.user,
            product=product,
            message=message
        )
