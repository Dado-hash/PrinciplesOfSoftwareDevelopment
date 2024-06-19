from typing import Any
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_of_measure = models.CharField(max_length=10, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    always_in_stock = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default="New")
    category = models.CharField(max_length=100, null=True, blank=True)
    storage_location = models.CharField(max_length=100, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.pk:
            old_product = Product.objects.get(pk=self.pk)
            old_expiration_date = old_product.expiration_date
            if old_expiration_date is not None:
                Notification.objects.filter(
                    user=self.user,
                    product=self,
                    message__contains=old_expiration_date
                ).delete()

        super(Product, self).save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.capitalize()
        super(ShoppingList, self).save(*args, **kwargs)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

