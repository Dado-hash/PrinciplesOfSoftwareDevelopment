from django.contrib import admin
from .models import Product, Profile, ShoppingList

admin.site.register(Product)
admin.site.register(ShoppingList)
admin.site.register(Profile)
