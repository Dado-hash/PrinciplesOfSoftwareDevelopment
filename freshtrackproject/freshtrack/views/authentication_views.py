from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from freshtrack.forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.urls import reverse
from freshtrack.forms import RegisterForm

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

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not username:
            messages.error(request, 'Username cannot be empty.')
            return render(request, 'registration/login.html')
        
        if not password:
            messages.error(request, 'Password cannot be empty.')
            return render(request, 'registration/login.html', {'username': username})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Invalid username or password
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'registration/login.html', {'username': username})
    else:
        return render(request, 'registration/login.html')
    
@login_required
def logout(request):
    logout(request)
    return redirect('login')