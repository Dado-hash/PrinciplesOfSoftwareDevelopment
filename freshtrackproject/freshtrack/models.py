from django.db import models
from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    expiration_date = models.DateField()
    insertion_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100)
    storage_location = models.CharField(max_length=100)
    always_in_stock = models.BooleanField(default=False)  # Nuovo campo per indicare se il prodotto deve essere sempre in dispensa

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    added_date = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)