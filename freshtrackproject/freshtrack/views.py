import time

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm, ShoppingListForm
from .models import Product, ShoppingList


def index(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'registration/login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'registration/login.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save(commit=False)
            print(user)
            user.is_staff = False
            user.is_superuser = False
            user.save()
            return redirect("/login")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def home(request):
    # Qui inserisci il codice per renderizzare la home
    pantry_items = Product.objects.filter(user=request.user)
    shopping_items = ShoppingList.objects.filter(user=request.user)
    return render(request, 'home.html', {'pantry_items': pantry_items, 'shopping_items': shopping_items})

@login_required
def logout(request):
    logout(request)
    return redirect('login')


@login_required
def add_to_shopping_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            shopping_item = form.save(commit=False)
            shopping_item.user = request.user
            shopping_item.save()
            return redirect('home')
    else:
        form = ShoppingListForm()
    return render(request, 'home.html', {'form': form})

@login_required
def update_shopping_list(request, product_id):
    product = Product.objects.get(pk=product_id)
    if product.user == request.user and product.quantity == 0 and not product.always_in_stock:
        shopping_item = ShoppingList(user=request.user, product_name=product.name, quantity=1)
        shopping_item.save()
    return redirect('home')

@login_required
def remove_from_shopping_list(request, item_id):
    shopping_item = ShoppingList.objects.get(pk=item_id)
    if shopping_item.user == request.user:
        shopping_item.delete()
    return redirect('shopping_list')

@login_required
def mark_as_purchased(request, item_id):
    shopping_item = ShoppingList.objects.get(pk=item_id)
    if shopping_item.user == request.user:
        shopping_item.purchased = True
        shopping_item.save()
    return redirect('shopping_list')

@login_required
def product_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        if 'always_in_stock' in request.POST:
            product.always_in_stock = True
            product.save()
            return redirect('product_detail', product_id=product_id)
    return render(request, 'product_detail.html', {'product': product})


@login_required
def add_to_pantry(request):
    if request.method == 'POST':
        # Ricevi i dati dal form
        product_name = request.POST.get('product_name')
        expiration_date = request.POST.get('expiration_date')
        quantity = request.POST.get('quantity')
        unit_of_measure = request.POST.get('unit_of_measure')

        # Crea un nuovo oggetto Product nella dispensa dell'utente corrente
        Product.objects.create(
            user=request.user,
            name=product_name,
            expiration_date=expiration_date,
            quantity=quantity,
            unit_of_measure=unit_of_measure
        )

        # Reindirizza l'utente alla home o alla pagina della dispensa
        return redirect('home')  # Puoi cambiare 'home' con la URL della pagina della dispensa se necessario

    return render(request, 'home.html')  # Renderizza il template del form per aggiungere alla dispensa

@login_required
def remove_from_pantry(request, product_id):
    product = Product.objects.get(pk=product_id)
    if product.user == request.user:
        # Se l'attributo always_in_stock è attivo, aggiungi l'oggetto alla lista della spesa
        if product.always_in_stock:
            shopping_item = ShoppingList.objects.create(
                user=request.user,
                product_name=product.name,
                quantity=1,  # Puoi modificare la quantità in base alle tue esigenze
                unit_of_measure=product.unit_of_measure
            )
            shopping_item.save()
        # Rimuovi l'oggetto dalla dispensa
        product.delete()
    return redirect('home')

