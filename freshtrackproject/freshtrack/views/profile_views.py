from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from freshtrack.tasks import check_expirations
from freshtrack.forms import ProfileUpdateForm
from freshtrack.models import Product, ShoppingList
from django.contrib import messages

@login_required
def profile(request):
    profile = request.user.profile
    return render(request, 'profile.html', {'profile': profile})

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'profile.html', {
        'profile': request.user.profile,
    })

@login_required
def home(request):
    check_expirations()
    pantry_items = Product.objects.filter(user=request.user)
    shopping_items = ShoppingList.objects.filter(user=request.user)
    return render(request, 'home.html', {'pantry_items': pantry_items, 'shopping_items': shopping_items})