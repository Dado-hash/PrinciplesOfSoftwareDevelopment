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

PRODUCT_CATEGORY_MAP = {
    'apple': 'Fruit',
    'banana': 'Fruit',
    'orange': 'Fruit',
    'grape': 'Fruit',
    'watermelon': 'Fruit',
    'strawberry': 'Fruit',
    'blueberry': 'Fruit',
    'raspberry': 'Fruit',
    'kiwi': 'Fruit',
    'pear': 'Fruit',
    'peach': 'Fruit',
    'plum': 'Fruit',
    'cherry': 'Fruit',
    'mango': 'Fruit',
    'pineapple': 'Fruit',
    'lemon': 'Fruit',
    'lime': 'Fruit',
    'grapefruit': 'Fruit',
    'tomato': 'Vegetable',
    'carrot': 'Vegetable',
    'broccoli': 'Vegetable',
    'cauliflower': 'Vegetable',
    'spinach': 'Vegetable',
    'lettuce': 'Vegetable',
    'kale': 'Vegetable',
    'cabbage': 'Vegetable',
    'celery': 'Vegetable',
    'cucumber': 'Vegetable',
    'zucchini': 'Vegetable',
    'eggplant': 'Vegetable',
    'pepper': 'Vegetable',
    'onion': 'Vegetable',
    'garlic': 'Vegetable',
    'potato': 'Vegetable',
    'sweet potato': 'Vegetable',
    'yam': 'Vegetable',
    'corn': 'Vegetable',
    'pea': 'Vegetable',
    'bean': 'Vegetable',
    'lentil': 'Vegetable',
    'chickpea': 'Vegetable',
    'soybean': 'Vegetable',
    'tofu': 'Vegetable',
    'tempeh': 'Vegetable',
    'mushroom': 'Vegetable',
    'avocado': 'Fruit',
    'bread': 'Bakery',
    'bagel': 'Bakery',
    'croissant': 'Bakery',
    'muffin': 'Bakery',
    'donut': 'Bakery',
    'biscuit': 'Bakery',
    'scone': 'Bakery',
    'tortilla': 'Bakery',
    'rice': 'Grain',
    'pasta': 'Grain',
    'noodle': 'Grain',
    'quinoa': 'Grain',
    'oatmeal': 'Grain',
    'barley': 'Grain',
    'wheat': 'Grain',
    'flour': 'Grain',
    'milk': 'Dairy',
    'cheese': 'Dairy',
    'yogurt': 'Dairy',
    'butter': 'Dairy',
    'cream': 'Dairy',
    'egg': 'Dairy',
    'beef': 'Meat',
    'pork': 'Meat',
    'chicken': 'Meat',
    'turkey': 'Meat',
    'lamb': 'Meat',
    'duck': 'Meat',
    'sausage': 'Meat',
    'bacon': 'Meat',
    'ham': 'Meat',
    'salami': 'Meat',
    'fish': 'Seafood',
    'salmon': 'Seafood',
    'tuna': 'Seafood',
    'shrimp': 'Seafood',
    'crab': 'Seafood',
    'lobster': 'Seafood',
    'clam': 'Seafood',
    'oyster': 'Seafood',
    'scallop': 'Seafood',
    'trout': 'Seafood',
    'cod': 'Seafood',
    'olive oil': 'Condiment',
    'vinegar': 'Condiment',
    'ketchup': 'Condiment',
    'mustard': 'Condiment',
    'mayonnaise': 'Condiment',
    'soy sauce': 'Condiment',
    'hot sauce': 'Condiment',
    'sugar': 'Baking',
    'salt': 'Baking',
    'pepper': 'Spice',
    'cinnamon': 'Spice',
    'nutmeg': 'Spice',
    'ginger': 'Spice',
    'turmeric': 'Spice',
    'basil': 'Herb',
    'parsley': 'Herb',
    'cilantro': 'Herb',
    'rosemary': 'Herb',
    'thyme': 'Herb',
    'oregano': 'Herb',
    'mint': 'Herb'
}

