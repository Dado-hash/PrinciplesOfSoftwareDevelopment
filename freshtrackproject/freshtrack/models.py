from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    UNIT_CHOICES = [
        ('L', 'Litri'),
        ('g', 'Grammi'),
        ('u', 'Unità'),
    ]

    STATUS_CHOICES = [
        ('New', 'New'),
        ('Opened', 'Opened'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_of_measure = models.CharField(max_length=1, choices=UNIT_CHOICES)
    expiration_date = models.DateField(blank=True, null=True, default=None) 
    insertion_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    storage_location = models.CharField(max_length=100, blank=True, null=True)
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
    always_in_stock = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'

