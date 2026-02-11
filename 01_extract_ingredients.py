import google.generativeai as genai

from PIL import Image

import io

"""Sample output able to produce:
Ingredients: {"itemName": "Paneer 65", "ingredients": ["Paneer (Indian cottage cheese)", "Yogurt", "Ginger-Garlic Paste", "Red Chili Powder", "Turmeric Powder", "Garam Masala", "Salt", "Lemon Juice", "Rice Flour", "Cornstarch", "Cooking Oil", "Curry Leaves", "Green Chilies", "Cashews", "Fresh Coriander Leaves"]}

or

{"itemName": "Not a food item", "ingredients":}
"""

# Configure Gemini API

genai.configure(api_key='AIzaSyBjSsg5RJVWvgVMVMdxizxvg1tgHSrSSbI')

# Load image and identify food item

model = genai.GenerativeModel('gemini-2.5-flash')

image_path = 'dmla.jpg'  # replace with your image path

image = Image.open(image_path)
image_byte_arr = io.BytesIO()
image.save(image_byte_arr, format='JPEG')
image_blob = image_byte_arr.getvalue()

SYSTEM_PROMPT = """
you are an expert in identifying food items from images. Given an image, you will identify the food item and list its ingredients.

You need to follow the output format strictly, Nothing else should come after the output, Below is the format you need to follow:

Example Output:
{"itemName": "Pizza", "ingredients": ["Flour", "Tomato Sauce", "Cheese", "Olive Oil", "Yeast", "Salt"]}
{"itemName": "Caesar Salad", "ingredients": ["Romaine Lettuce", "Croutons", "Parmesan Cheese", "Caesar Dressing", "Lemon Juice", "Olive Oil", "Garlic"]}
{"itemName": "Not a food item.", "ingredients":}

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

print('Ingredients:', ingredients)
 