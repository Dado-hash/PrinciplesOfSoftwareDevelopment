from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    UNIT_CHOICES = [
        ('L', 'Litri'),
        ('g', 'Grammi'),
        ('u', 'Unità'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_of_measure = models.CharField(max_length=1, choices=UNIT_CHOICES)
    expiration_date = models.DateField()
    insertion_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100)
    storage_location = models.CharField(max_length=100)
    always_in_stock = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ShoppingList(models.Model):
    UNIT_CHOICES = [
        ('L', 'Litri'),
        ('g', 'Grammi'),
        ('u', 'Unità'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_of_measure = models.CharField(max_length=1, choices=UNIT_CHOICES)
    added_date = models.DateTimeField(auto_now_add=True)
    purchased = models.BooleanField(default=False)
