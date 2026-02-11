document.getElementById('upload-form').addEventListener('submit', async (e) => {
   console.log("form Submit event caught!!");
   e.preventDefault();
   const formData = new FormData(e.target);
   const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Processing...</p>';
   try {
       const response = await fetch('http://127.0.0.1:5000/extract/ingredients', {
           method: 'POST',
           body: formData
       });
       const data = await response.json();
       console.log(data);
    //    const resultDiv = document.getElementById('result');
       resultDiv.innerHTML = `
<h2>${data.foodName} for ${data.noOfPersons} number of people </h2>
<h2>Want to know the recipe: <a href="#" id="recipeToggle">Click Here</a></h2>
<div id="recipeText" style="display:none; white-space:pre-wrap;">${data.recipe}</div>
<table>
<thead>
<tr>
<th>Item Name</th>
<th>Quantity</th>
<th>is Allergen?</th>
<th>Add to cart?</th>
</tr>
</thead>
<tbody>
 ${data.ingredients.map(item => `
<tr>
<td>${item.itemName}</td>
<td>${item.qty}</td>
<td>${item.allergen}</td>
<td><button onclick="addToCart('${item.itemName}')">Add to Cart</button></td>
</tr>
 `).join('')}
</tbody>
</table>
       `;
       document.getElementById('recipeToggle').addEventListener('click', (e) => {
 e.preventDefault();
 const recipeDiv = document.getElementById('recipeText');
 recipeDiv.style.display = recipeDiv.style.display === 'none' ? 'block' : 'none';
});
   } catch (error) {
       console.error('Error:', error);
   }
});