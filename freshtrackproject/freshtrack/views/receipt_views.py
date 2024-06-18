import json
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from freshtrack.forms import UploadReceiptForm
from freshtrack.models import Product
from django.views.decorators.csrf import csrf_exempt
from freshtrack.utility import extract_products_from_receipt
from django.core.files.storage import FileSystemStorage

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

