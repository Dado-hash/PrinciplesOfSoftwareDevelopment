from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from freshtrack.forms import ShoppingListForm
from freshtrack.models import Product, ShoppingList
from django.contrib import messages
from django.http import Http404
from freshtrack.tasks import check_expirations

@login_required
def add_to_shopping_list(request):
    if request.method == 'POST':
        form = ShoppingListForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name'].capitalize()
            quantity = form.cleaned_data['quantity']
            unit_of_measure = form.cleaned_data['unit_of_measure']

            # Cerca un prodotto esistente con lo stesso nome e unità di misura
            shopping_item = ShoppingList.objects.filter(
                user=request.user,
                product_name=product_name,
                unit_of_measure=unit_of_measure
            ).first()

            if shopping_item:
                # Se il prodotto esiste, aggiorna la quantità
                shopping_item.quantity += quantity
                shopping_item.save()
            else:
                # Crea un nuovo oggetto ShoppingList per l'utente corrente
                shopping_item = form.save(commit=False)
                shopping_item.user = request.user
                shopping_item.product_name = product_name
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
            check_expirations()
            messages.success(request, 'Item updated successfully')
            # Reindirizza l'utente alla pagina di dettaglio dell'elemento della lista della spesa appena modificato
            return redirect('shopping_list_item_detail', item_id=item.id)
    else:
        # Se il metodo della richiesta non è POST, significa che è una richiesta GET e l'utente sta solo visualizzando il modulo
        form = ShoppingListForm(instance=item)

    check_expirations()
    
    # Passa il modulo compilato o vuoto al template
    return render(request, 'shopping_list_item_detail.html', {'form': form})

@login_required
def mark_as_purchased(request, item_id):
    try:
        shopping_item = ShoppingList.objects.get(pk=item_id)
    except ShoppingList.DoesNotExist:
        raise Http404("ShoppingList item with id {} does not exist".format(item_id))
    
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
