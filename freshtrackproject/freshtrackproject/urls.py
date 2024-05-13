"""
URL configuration for freshtrackproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from freshtrack.views import about, index, logout, mark_as_not_purchased, mark_as_purchased, pantry, register, home, add_to_pantry, add_to_shopping_list, remove_and_add_to_pantry, remove_from_pantry, remove_from_pantry_page, remove_from_shopping_list, move_to_shopping_list, pantry_product_detail, shopping_list_item_detail, edit_shopping_list_item, update_product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('', include("django.contrib.auth.urls")),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('logout/', logout, name='logout'),
    path('add_to_pantry', add_to_pantry, name='add_to_pantry'),
    path('remove_from_pantry/<int:product_id>/', remove_from_pantry, name='remove_from_pantry'),
    path('remove_and_add_to_pantry/', remove_and_add_to_pantry, name='remove_and_add_to_pantry'),
    path('mark_as_purchased/<int:item_id>/', mark_as_purchased, name='mark_as_purchased'),
    path('mark_as_not_purchased/<int:item_id>/', mark_as_not_purchased, name='mark_as_not_purchased'),
    path('remove_from_shopping_list/<int:item_id>/', remove_from_shopping_list, name='remove_from_shopping_list'),
    path('add_to_shopping_list', add_to_shopping_list, name='add_to_shopping_list'),
    path('move_to_shopping_list/<int:item_id>/', move_to_shopping_list, name='move_to_shopping_list'),
    path('pantry_product_detail/<int:item_id>/', pantry_product_detail, name='pantry_product_detail'),
    path('shopping_list_item_detail/<int:item_id>/', shopping_list_item_detail, name='shopping_list_item_detail'),
    path('edit_shopping_list_item/<int:item_id>/', edit_shopping_list_item, name='edit_shopping_list_item'),
    path('update_product/<int:item_id>/', update_product, name='update_product'),
    path('pantry/', pantry, name='pantry'),
    path('remove_from_pantry_page/<int:product_id>/', remove_from_pantry_page, name='remove_from_pantry_page'),
]