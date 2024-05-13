def categorize_string(input_string):
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

# Esempio di utilizzo della funzione
input_string = 'parola2'
categoria = categorize_string(input_string)
if categoria:
    print(f'La stringa "{input_string}" appartiene alla categoria: {categoria}')
else:
    print(f'La stringa "{input_string}" non appartiene a nessuna categoria.')
