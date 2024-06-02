
from .models import Product, Notification
import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function that return the food category of a product
def food_categories (input_string):
    food_categories = {
        "Fruit": ["apple", "banana", "orange", "strawberry", "grape"],
        "Vegetable": ["carrot", "tomato", "spinach", "broccoli", "cucumber"],
        "Meat": ["beef", "pork", "chicken", "lamb", "venison"],
        "Fish and Seafood": ["salmon", "tuna", "cod", "shrimp", "oyster"],
        "Dairy Products": ["milk", "cheese", "yogurt", "butter", "cream"],
        "Grains and Derivatives": ["rice", "wheat", "corn", "pasta", "bread"],
        "Legumes": ["beans", "lentils", "chickpeas", "peas", "soybeans"],
        "Snacks and Sweets": ["cookies", "chocolate", "candy", "chips", "popcorn"],
        "Beverages": ["water", "fruit juice", "soda", "tea", "coffee"]
    }

    for category, word_list in food_categories.items():
        if input_string.lower() in word_list:
            return category
    
    # If the string does not match any category, return None
    return None

def findObjectPantry(name):
    try:
        product = Product.objects.get(name=name.capitalize())
        return product
    except Product.DoesNotExist:
        return None

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