
from .models import Product, Notification
import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_notifications_for_user(user):
    return Notification.objects.filter(user=user, is_read=False).order_by('-timestamp')

def extract_products_from_receipt(image_path):
    # Usa Tesseract per estrarre il testo dall'immagine
    text = pytesseract.image_to_string(Image.open(image_path))
    
    # Dividi il testo in righe
    lines = text.split('\n')
    
    # Lista per conservare i nomi dei prodotti
    products = []

    # Cerca di estrarre i nomi dei prodotti dalle righe
    for line in lines:
        # Usa espressioni regolari per trovare nomi di prodotti
        # Adatta questo pattern in base alla struttura degli scontrini
        match = re.match(r'^[a-zA-Z\s]+$', line)
        if match:
            product_name = line.strip().capitalize()
            products.append(product_name)

    return products