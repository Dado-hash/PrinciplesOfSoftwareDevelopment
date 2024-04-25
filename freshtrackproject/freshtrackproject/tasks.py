# tasks.py

from datetime import date
from django.utils import timezone
from freshtrack.models import Product, ShoppingList
from celery import Celery
from celery.schedules import crontab

def check_expired_products_and_add_to_shopping_list():
    today = date.today()
    expired_products = Product.objects.filter(expiration_date__lte=today, always_in_stock=True)

    for product in expired_products:
        # Controlla se il prodotto è già stato aggiunto alla lista della spesa
        already_added = ShoppingList.objects.filter(user=product.user, product_name=product.name,
                                                    added_date=today).exists()
        if not already_added:
            shopping_item = ShoppingList(user=product.user, product_name=product.name, quantity=1, added_date=today)
            shopping_item.save()


def setup_periodic_tasks(sender, **kwargs):

    app = Celery('tasks', broker='redis://localhost:6379/0')

    @app.on_after_configure.connect
    def setup_periodic_tasks(sender, **kwargs):
        sender.add_periodic_task(crontab(hour=0, minute=0), check_expired_products_and_add_to_shopping_list.s())
