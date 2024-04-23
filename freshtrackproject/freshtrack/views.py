import time
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegistrationForm


def index(request):
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('login'))  # Assicurati che 'login' sia il nome corretto della tua vista di login
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})
