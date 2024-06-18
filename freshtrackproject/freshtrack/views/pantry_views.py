from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.dateparse import parse_date
from freshtrack.forms import EditProductForm
from freshtrack.models import Product, ShoppingList
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

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
def pantry_product_detail(request, item_id):
    item = get_object_or_404(Product, pk=item_id)
    return render(request, 'product_detail.html', {'item': item})

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