import time
import json
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.dateparse import parse_date

from freshtrack.tasks import check_expirations
from .forms import EditProductForm, RegisterForm, ShoppingListForm, UploadReceiptForm
from .models import Product, ShoppingList
from django.utils.datastructures import MultiValueDictKeyError
from .utility import get_notifications_for_user
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .utility import extract_products_from_receipt
from django.core.files.storage import FileSystemStorage


def index(request):
    check_expirations()
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

def about(request):
    return render(request, 'about.html')

@login_required
def home(request):
    check_expirations()
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
        expiration_date_str = request.POST.get('expiration_date')
        # Converte la stringa della data in un oggetto datetime
        expiration_date = parse_date(expiration_date_str)
        quantity = request.POST.get('quantity')
        unit_of_measure = request.POST.get('unit_of_measure')
        always_in_stock = request.POST.get('always_in_stock')
        storage_location = request.POST.get('storage_location')

        # Cerca un prodotto esistente con lo stesso nome, unità di misura e data di scadenza
        product = Product.objects.filter(
            user=request.user,
            name=product_name.capitalize(),
            expiration_date=expiration_date,
            unit_of_measure=unit_of_measure,
            storage_location=storage_location
        ).first()

        if product:
            # Se il prodotto esiste, aggiorna la quantità
            product.quantity += int(quantity)
            product.save()
        else:
            # Crea un nuovo oggetto Product nella dispensa dell'utente corrente
            Product.objects.create(
                user=request.user,
                name=product_name.capitalize(),
                expiration_date=expiration_date if expiration_date_str else None,  # Imposta None se la stringa della data è vuota
                quantity=quantity,
                unit_of_measure=unit_of_measure,
                always_in_stock=always_in_stock,
                status="New",
                category='',
                storage_location=storage_location
            )

        # Reindirizza l'utente alla home o alla pagina della dispensa
        return redirect('home')

    return render(request, 'home.html')  # Renderizza il template del form per aggiungere

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
def remove_from_pantry_page(request, product_id):
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
    return redirect('pantry')

@login_required
def remove_and_add_to_pantry(request):
    if request.method == 'POST':
        # Recupera gli elementi contrassegnati come acquistati dalla lista della spesa
        purchased_items = ShoppingList.objects.filter(user=request.user, purchased=True)
        for item in purchased_items:
            # Cerca un prodotto esistente con lo stesso nome, unità di misura e posizione di archiviazione
            product = Product.objects.filter(
                user=request.user,
                name=item.product_name.capitalize(),
                unit_of_measure=item.unit_of_measure,
                storage_location='Pantry'
            ).first()

            if product:
                # Se il prodotto esiste, aggiorna la quantità
                product.quantity += item.quantity
                product.save()
            else:
                # Aggiungi ogni elemento alla dispensa come oggetto Product
                Product.objects.create(
                    user=request.user,
                    name=item.product_name.capitalize(),
                    quantity=item.quantity,
                    unit_of_measure=item.unit_of_measure,
                    expiration_date=None,
                    always_in_stock=item.always_in_stock,
                    status='New',
                    category='',
                    storage_location='Pantry'
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

@login_required
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

@login_required
def pantry_product_detail(request, item_id):
    item = get_object_or_404(Product, pk=item_id)
    return render(request, 'product_detail.html', {'item': item})

@login_required
def shopping_list_item_detail(request, item_id):
    item = get_object_or_404(ShoppingList, pk=item_id)
    return render(request, 'shopping_list_item_detail.html', {'item': item})

@login_required
def edit_shopping_list_item(request, item_id):
    # Recupera l'istanza dell'elemento della lista della spesa
    item = get_object_or_404(ShoppingList, id=item_id)
    
    if request.method == 'POST':
        # Se il metodo della richiesta è POST, significa che l'utente ha inviato il modulo con i dati aggiornati
        form = ShoppingListForm(request.POST, instance=item)
        if form.is_valid():
            # Salva i dati aggiornati dell'elemento della lista della spesa nel database
            form.save()
            messages.success(request, 'Item updated successfully')
            # Reindirizza l'utente alla pagina di dettaglio dell'elemento della lista della spesa appena modificato
            return redirect('shopping_list_item_detail', item_id=item.id)
    else:
        # Se il metodo della richiesta non è POST, significa che è una richiesta GET e l'utente sta solo visualizzando il modulo
        form = ShoppingListForm(instance=item)
    
    # Passa il modulo compilato o vuoto al template
    return render(request, 'shopping_list_item_detail.html', {'form': form})

@login_required
def update_product(request, item_id):
    # Recupera l'istanza del prodotto
    item = get_object_or_404(Product, id=item_id)
    
    if request.method == 'POST':
        # Se il metodo della richiesta è POST, significa che l'utente ha inviato il modulo con i dati aggiornati
        form = EditProductForm(request.POST, instance=item)
        if form.is_valid():
            # Controllo e sostituzione dei valori None con la stringa vuota ""
            try:
                if not form.cleaned_data['category']:
                    form.cleaned_data['category'] = ''
            except MultiValueDictKeyError:
                pass
            
            try:
                if not form.cleaned_data['storage_location']:
                    form.cleaned_data['storage_location'] = ''
                    print(form.cleaned_data['storage_location'])
            except MultiValueDictKeyError:
                pass
            
            # Salva i dati aggiornati del prodotto nel database
            form.save()
            messages.success(request, 'Item updated successfully')
            # Reindirizza l'utente alla pagina di dettaglio del prodotto appena modificato
            return redirect('pantry_product_detail', item_id=item.id)
    else:
        # Se il metodo della richiesta non è POST, significa che è una richiesta GET e l'utente sta solo visualizzando il modulo
        form = EditProductForm(instance=item)
    
    # Il form è invalido, passa il form compilato e gli errori al template
    return render(request, 'product_detail.html', {'form': form, 'item': item, 'errors': form.errors})


@login_required
def pantry(request):
    # Recupera l'utente attualmente autenticato
    user = request.user

    # Recupera tutti i prodotti nella dispensa dell'utente
    pantry_items = Product.objects.filter(user=user)

    # Recupera le categorie uniche dei prodotti nella dispensa dell'utente
    categories = pantry_items.values_list('category', flat=True).distinct()

    # Recupera le posizioni di archiviazione uniche dei prodotti nella dispensa dell'utente
    storage_locations = ["Pantry", "Fridge", "Freezer", "Spices", "Beverages", "Other"]

    # Applica i filtri se sono presenti nei parametri GET
    category_filter = request.GET.get('category')
    storage_location_filter = request.GET.get('storage_location')

    if category_filter:
        pantry_items = pantry_items.filter(category=category_filter)
    if storage_location_filter:
        pantry_items = pantry_items.filter(storage_location=storage_location_filter)

    # Passa i prodotti nella dispensa, le categorie e le posizioni di archiviazione filtrati come contesto al template
    return render(request, 'pantry.html', {
        'pantry_items': pantry_items,
        'categories': categories,
        'storage_locations': storage_locations,
        'selected_category': category_filter,  # Passa il valore selezionato per il filtro categoria
        'selected_storage_location': storage_location_filter,  # Passa il valore selezionato per il filtro di posizione di archiviazione
    })

def notifications_view(request):
    notifications = get_notifications_for_user(request.user)
    return render(request, 'notifications.html', {
        'notifications': notifications,
    })


@login_required
@csrf_exempt
def add_product_barcode(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        barcode = data.get('barcode')

        # Ricerca del prodotto tramite API esterna
        response = requests.get(f'https://world.openfoodfacts.org/api/v0/product/{barcode}.json')
        if response.status_code == 200:
            product_data = response.json()

            if product_data.get('status') == 1:
                product_info = product_data.get('product')
                user = request.user  # Ottieni l'utente autenticato
                product = Product.objects.create(
                    user=user,
                    name=product_info.get('product_name', f'Product with barcode {barcode}'),
                    quantity=1,
                    unit_of_measure='u',
                    status='New',
                    category=product_info.get('categories', ''),
                    notes=product_info.get('ingredients_text', ''),
                    storage_location='Pantry',
                    always_in_stock=False,
                    expiration_date=None
                )
                return JsonResponse({'status': 'success', 'redirect_url': '/home/'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
        else:
            return JsonResponse({'status': 'error', 'message': 'API request failed'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def scanner(request):
    return render(request, 'scanner.html')

@login_required
def upload_receipt(request):
    if request.method == 'POST':
        form = UploadReceiptForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva l'immagine caricata
            receipt_image = form.cleaned_data['receipt_image']
            fs = FileSystemStorage()
            filename = fs.save(receipt_image.name, receipt_image)
            uploaded_file_url = fs.url(filename)

            # Estrai i prodotti dall'immagine dello scontrino
            products = extract_products_from_receipt(fs.path(filename))
            # Aggiungi i prodotti alla dispensa
            for product_name in products:
                Product.objects.create(
                    user=request.user,
                    name=product_name,
                    quantity=1,
                    unit_of_measure='u',
                    status='New',
                    category='',
                    storage_location='Pantry'
                )
            # Elimina il file dopo l'elaborazione
            if fs.exists(filename):
                fs.delete(filename)
            
            return HttpResponseRedirect('/home/')
    else:
        form = UploadReceiptForm()
    return render(request, 'upload_receipt.html', {'form': form})