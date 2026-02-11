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
    NoOfPersons = request.form.get('persons')
    #image_path = 'dmla.jpg'  

    image = Image.open(image_path)
    image_byte_arr = io.BytesIO()
    image.save(image_byte_arr, format='JPEG')
    image_blob = image_byte_arr.getvalue()

    SYSTEM_PROMPT = """
    you are an expert in identifying food items from images. Given an image, you will identify the food item and list its ingredients also if it contains any allergetic items and receipe step wise with line break <\br> as well.

    You need to follow the output format strictly, Nothing else should come after the output, Below is the format you need to follow:

    Example Output:
    {"foodName": "Pizza","noOfPersons": 2,"recipe": "Mix flour with yeast and water,</br>Let it rise for 1 hour.</br>Roll out the dough and add tomato sauce, cheese, and toppings.</br>Bake at 220°C for 15 minutes.","ingredients": [{"itemName":"Flour","qty":"1 kg", "allergen": false}, {"itemName":"Tomato Sauce","qty":"500 gm", "allergen": false}, {"itemName":"Cheese","qty":"200 gm", "allergen": true}, {"itemName":"Olive Oil","qty":"100 ml", "allergen": false}, {"itemName":"Yeast","qty":"7 gm", "allergen": false}, {"itemName":"Salt","qty":"to taste", "allergen": false}]}
    {"foodName": "Caesar Salad","noOfPersons": 2, "recipe": "Wash and chop romaine lettuce.</br>Mix croutons, parmesan cheese, and dressing.</br>Toss with lettuce and serve.","ingredients": [{"itemName":"Romaine Lettuce","qty":"1 head", "allergen": false}, {"itemName":"Croutons","qty":"100 gm", "allergen": true}, {"itemName":"Parmesan Cheese","qty":"50 gm", "allergen": true}, {"itemName":"Caesar Dressing","qty":"100 ml", "allergen": true}, {"itemName":"Lemon Juice","qty":"30 ml", "allergen": false}, {"itemName":"Olive Oil","qty":"50 ml", "allergen": false}, {"itemName":"Garlic","qty":"2 cloves", "allergen": false}]}
    {"foodName": "Not a food item", "ingredients":}

    """

    USER_PROMPT = f"What's this food item and its ingredients with their respective quantities and allergen information for {NoOfPersons} persons?"

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
 