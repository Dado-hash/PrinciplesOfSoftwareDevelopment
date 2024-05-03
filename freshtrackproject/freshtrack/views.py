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
def remove_from_shopping_list(request, item_id):
    shopping_item = ShoppingList.objects.get(pk=item_id)
    if shopping_item.user == request.user:
        shopping_item.delete()
    return redirect('home')

@login_required
def add_to_pantry(request):
    if request.method == 'POST':
        # Ricevi i dati dal form
        product_name = request.POST.get('product_name')
        expiration_date = request.POST.get('expiration_date')
        quantity = request.POST.get('quantity')
        unit_of_measure = request.POST.get('unit_of_measure')
        always_in_stock = request.POST.get('always_in_stock')

        # Crea un nuovo oggetto Product nella dispensa dell'utente corrente
        Product.objects.create(
            user=request.user,
            name=product_name,
            expiration_date=expiration_date,
            quantity=quantity,
            unit_of_measure=unit_of_measure,
            always_in_stock=always_in_stock
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
                unit_of_measure=product.unit_of_measure,
                always_in_stock=product.always_in_stock
            )
            shopping_item.save()
        # Rimuovi l'oggetto dalla dispensa
        product.delete()
    return redirect('home')

@login_required
def remove_and_add_to_pantry(request):
    if request.method == 'POST':
        # Recupera gli elementi contrassegnati come acquistati dalla lista della spesa
        purchased_items = ShoppingList.objects.filter(user=request.user, purchased=True)
        for item in purchased_items:
            # Aggiungi ogni elemento alla dispensa come oggetto Product
            Product.objects.create(
                user=request.user,
                name=item.product_name,
                quantity=item.quantity,
                unit_of_measure=item.unit_of_measure,
                expiration_date=None,
                always_in_stock=item.always_in_stock
            )
        # Rimuovi gli elementi contrassegnati come acquistati dalla lista della spesa
        purchased_items.delete()
    return redirect('home')

@login_required
def mark_as_purchased(request, item_id):
    shopping_item = ShoppingList.objects.get(pk=item_id)
    if shopping_item.user == request.user:
        shopping_item.purchased = True
        shopping_item.save()
    return redirect('home')

@login_required
def mark_as_not_purchased(request, item_id):
    try:
        shopping_item = ShoppingList.objects.get(pk=item_id, user=request.user)
        shopping_item.purchased = False
        shopping_item.save()
    except ShoppingList.DoesNotExist:
        pass
    return redirect('home')


def move_to_shopping_list(request, item_id):
    # Trova l'oggetto della dispensa da spostare
    pantry_item = Product.objects.get(id=item_id)

    # Crea un nuovo oggetto nella lista della spesa utilizzando i dati dalla dispensa
    ShoppingList.objects.create(
        user=request.user,
        product_name=pantry_item.name,
        quantity=pantry_item.quantity,
        unit_of_measure=pantry_item.unit_of_measure,
        always_in_stock=pantry_item.always_in_stock
    )
    pantry_item.delete()
    return redirect('home')
