import google.generativeai as genai

from PIL import Image

import io
from flask import Flask,request
from flask_cors import CORS


app = Flask(__name__)
# Configure Gemini API
CORS(app)
# genai.configure(api_key='AIzaSyBjSsg5RJVWvgVMVMdxizxvg1tgHSrSSbI')
genai.configure(api_key='AIzaSyABkpJuufZEOQB81TClObvnh4H-ePP39v0')

@app.route('/extract/ingredients', methods=['POST'])
def extract_ingredients_qty():



    """
    start flask server
    open new terminal
    python -m http.server 8000
    Sample output able to produce:
    Ingredients: {"foodName": "Paneer 65", "ingredients": [{itemName:"Paneer",qty:"250 gm"}, {itemName:"Cornflour",qty:"3 tbsp"}, {itemName:"Rice Flour",qty:"2 tbsp"}, {itemName:"Ginger Garlic Paste",qty:"1 tbsp"}, {itemName:"Red Chili Powder",qty:"1.5 tsp"}, {itemName:"Turmeric Powder",qty:"0.5 tsp"}, {itemName:"Curry Leaves",qty:"10-12 leaves"}, {itemName:"Green Chilies",qty:"2"}, {itemName:"Salt",qty:"to taste"}, {itemName:"Cooking Oil",qty:"for deep frying"}, {itemName:"Lemon Juice",qty:"1 tbsp"}, {itemName:"Coriander Leaves",qty:"2 tbsp"}, {itemName:"Cashew Nuts",qty:"10-12"}]}

    or

    {"itemName": "Not a food item", "ingredients":}
    """
    # Load image and identify food item

    model = genai.GenerativeModel('gemini-2.5-flash')
    image_path = request.files['image']
    #image_path = 'dmla.jpg'  

    image = Image.open(image_path)
    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format='JPEG')
    image_blob = image_byte_arr.getvalue()

    SYSTEM_PROMPT = """
    you are an expert in identifying food items from images. Given an image, you will identify the food item and list its ingredients.

    You need to follow the output format strictly, Nothing else should come after the output, Below is the format you need to follow:

    Example Output:
    {"foodName": "Pizza", "ingredients": [{"itemName":"Flour","qty":"1 kg"}, {"itemName":"Tomato Sauce","qty":"500 gm"}, {"itemName":"Cheese","qty":"200 gm"}, {"itemName":"Olive Oil","qty":"100 ml"}, {"itemName":"Yeast","qty":"7 gm"}, {"itemName":"Salt","qty":"to taste"}]}
    {"foodName": "Caesar Salad", "ingredients": [{"itemName":"Romaine Lettuce","qty":"1 head"}, {"itemName":"Croutons","qty":"100 gm"}, {"itemName":"Parmesan Cheese","qty":"50 gm"}, {"itemName":"Caesar Dressing","qty":"100 ml"}, {"itemName":"Lemon Juice","qty":"30 ml"}, {"itemName":"Olive Oil","qty":"50 ml"}, {"itemName":"Garlic","qty":"2 cloves"}]}
    {"foodName": "Not a food item", "ingredients":}

    """

    USER_PROMPT = "What's this food item and its ingredients with their respective quantities?"

    messages = [ 
        {"role": "model", "parts": [{"text": SYSTEM_PROMPT}]},
        {"role": "user", "parts": [
            {"text": USER_PROMPT}, 
            {"inline_data": {"mime_type": "image/jpeg", "data": image_blob}}
            ]}
    ]

    ingredients_qty_response = model.generate_content(messages)

    ingredients_qty = ingredients_qty_response.text

    print('Ingredients and Quantity:', ingredients_qty)
    return ingredients_qty

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
 