import google.generativeai as genai

from PIL import Image

import io

"""Sample output able to produce:
Ingredients: {"foodName": "Paneer 65", "ingredients": [{itemName:"Paneer",qty:"250 gm"}, {itemName:"Cornflour",qty:"3 tbsp"}, {itemName:"Rice Flour",qty:"2 tbsp"}, {itemName:"Ginger Garlic Paste",qty:"1 tbsp"}, {itemName:"Red Chili Powder",qty:"1.5 tsp"}, {itemName:"Turmeric Powder",qty:"0.5 tsp"}, {itemName:"Curry Leaves",qty:"10-12 leaves"}, {itemName:"Green Chilies",qty:"2"}, {itemName:"Salt",qty:"to taste"}, {itemName:"Cooking Oil",qty:"for deep frying"}, {itemName:"Lemon Juice",qty:"1 tbsp"}, {itemName:"Coriander Leaves",qty:"2 tbsp"}, {itemName:"Cashew Nuts",qty:"10-12"}]}

or

{"itemName": "Not a food item", "ingredients":}
"""

# Configure Gemini API

genai.configure(api_key='AIzaSyABkpJuufZEOQB81TClObvnh4H-ePP39v0')

# Load image and identify food item

model = genai.GenerativeModel('gemini-2.5-flash')

image_path = 'download.jpg'  

image = Image.open(image_path)
image_byte_arr = io.BytesIO()
image.save(image_byte_arr, format='JPEG')
image_blob = image_byte_arr.getvalue()

SYSTEM_PROMPT = """
you are an expert in identifying food items from images. Given an image, you will identify the food item and list its ingredients.

You need to follow the output format strictly, Nothing else should come after the output, Below is the format you need to follow:

Example Output:
{"itemName": "Paneer 65", "ingredients": ["Paneer (Indian cottage cheese)", "Yogurt", "Ginger-Garlic Paste", "Red Chili Powder", "Turmeric Powder", "Garam Masala", "Salt", "Lemon Juice", "Rice Flour", "Cornstarch", "Cooking Oil", "Curry Leaves", "Green Chilies", "Cashews", "Fresh Coriander Leaves"]}
{"itemName": "Not a food item", "ingredients":}

"""

USER_PROMPT = "What's this food item and its ingredients?"

messages = [ 
    {"role": "model", "parts": [{"text": SYSTEM_PROMPT}]},
    {"role": "user", "parts": [
        {"text": USER_PROMPT}, 
        {"inline_data": {"mime_type": "image/jpeg", "data": image_blob}}
        ]}
]

ingredients_response = model.generate_content(messages)

ingredients = ingredients_response.text

print('Ingredients', ingredients)
 