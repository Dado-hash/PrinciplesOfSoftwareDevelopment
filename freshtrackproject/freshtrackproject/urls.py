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
from freshtrack.views import index, logout, register, home, add_to_pantry, add_to_shopping_list, remove_from_pantry

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('', include("django.contrib.auth.urls")),
    path('register/', register, name='register'),
    path('home/', home, name='home'),
    path('logout/', logout, name='logout'),
    path('add_to_pantry', add_to_pantry, name='add_to_pantry'),
    path('remove_from_pantry/<int:product_id>/', remove_from_pantry, name='remove_from_pantry'),
    path('add_to_shopping_list', add_to_shopping_list, name='add_to_shopping_list')
]