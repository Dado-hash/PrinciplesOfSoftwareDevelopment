from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from freshtrack.forms import CustomAuthenticationForm, RegisterForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.urls import reverse
from freshtrack.forms import RegisterForm
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return redirect(reverse('login'))
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm

