document.addEventListener('DOMContentLoaded', function() {
    var addToCartButtons = document.querySelectorAll('[id^="add-to-cart-button-"]');
    addToCartButtons.forEach(function(addToCartButton) {
      addToCartButton.addEventListener('click', function(e) {
        e.preventDefault();
  
        var productId = this.id.split('-').pop();
        var tableId = document.getElementById('table-id-input-' + productId).value;
        var quantity = document.getElementById('quantity-input-' + productId).value;
  
        var requestData = {
          table_id: tableId,
          product_id: productId,
          quantity: quantity
        };
  
        fetch('http://127.0.0.1:8000/cart/api/add-to-cart/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData)
        })
          .then(function(response) {
            if (response.ok) {
              console.log('تم الإضافة إلى السلة');
              var parentElement = addToCartButton.parentElement;
              var alertDiv = document.createElement('div');
              alertDiv.classList.add('alert', 'alert-success');
              alertDiv.innerHTML = '<span>تم الإضافة إلى السلة</span>';
              parentElement.insertBefore(alertDiv, addToCartButton.nextSibling);
  
              setTimeout(function() {
                alertDiv.style.display = 'none';
              }, 1000);
  
              // Perform any additional actions or UI updates here
            } else {
              throw new Error('Error adding item to cart.');
            }
          })
          .catch(function(error) {
            console.error('Error adding item to cart:', error.message);
            // Handle error and display appropriate message to the user
          });
      });
    });
  });


  document.addEventListener('DOMContentLoaded', function() {
    var cartButton = document.getElementById('cart-button');
    var modal = document.getElementById('cart-modal');
    var modalContent = document.querySelector('#cart-modal .modal-content');
    var closeButton = document.querySelector('#cart-modal .close');
  
    cartButton.addEventListener('click', function() {
      var tableId = document.getElementById('table-id-input').value;
      fetch('http://127.0.0.1:8000/cart/api/cart-items/' + tableId +'/')  // Replace 'cartId' with the actual cart ID
        .then(function(response) {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Error fetching cart items.');
          }
        })
        .then(function(data) {
          // Process the cart items data
          displayCartItems(data);
          modal.style.display = 'block';
        })
        .catch(function(error) {
          console.error('Error fetching cart items:', error.message);
          // Handle error and display appropriate message to the user
        });
    });
  
    closeButton.addEventListener('click', function() {
      modal.style.display = 'none';
    });
  
    window.addEventListener('click', function(event) {
      if (event.target === modal) {
        modal.style.display = 'none';
      }
    });

    function updateCartItemQuantity(itemId, quantityChange, data) {
      var payload = {
        itemId: itemId,
        quantityChange: quantityChange
      };
    
      // Make an AJAX POST request to the Django view URL
      $.ajax({
        url: 'http://127.0.0.1:8000/cart/update-cart-item-quantity/',
        type: 'POST',
        data: payload,
        dataType: 'json',
        success: function(response) {
          // Handle the success response
          console.log(response.message); // Output the success message
        },
        error: function(xhr, status, error) {
          // Handle the error response
          console.error('Error:', error); // Output the error message
        }
      });
    
      // Find the cart item with the matching itemId
      var cartItem = data.find(function(item) {
        return item.id === parseInt(itemId);
      });
    
      if (cartItem) {
        var newQuantity = cartItem.quantity + quantityChange;
         // Check if the new quantity is zero
         if (newQuantity === 0) {
          var cartItemCard = document.querySelector('.card.card-' + itemId);
          cartItemCard.remove();
          data[data.length - 1].total_price-=cartItem.price;
          var totalDiv = document.querySelector('#total-price .card');
          totalDiv.textContent = 'تكلفة الفاتورة: ' + data[data.length - 1].total_price;

        }
    
        // Ensure the new quantity is not negative
        if (newQuantity > 0) {
          cartItem.quantity = newQuantity;
          cartItem.total_price = cartItem.quantity * cartItem.price; // Update the total price based on the new quantity
    
          // Update the cart item display
          var quantityDiv = document.querySelector(`#cart-items [data-item-id="${itemId}"] + div`);
          var totalPriceDiv = document.querySelector(`#cart-items [data-item-id="${itemId}"] + div + div`);
          quantityDiv.innerHTML = '<strong>العدد:</strong> ' + cartItem.quantity;
          totalPriceDiv.innerHTML = '<strong>سعر الكل:</strong> ' + cartItem.total_price;

    
          // Update the total price display
          var totalPrice = data[data.length - 1].total_price;
          if(-1=== parseInt(quantityChange)){
          data[data.length - 1].total_price-=cartItem.price;
        }
          else
          {
            data[data.length - 1].total_price+=cartItem.price;
        }
        var totalDiv = document.querySelector('#total-price .card');
          totalDiv.textContent = 'تكلفة الفاتورة: ' + data[data.length - 1].total_price;
        }
      }
    }
function displayCartItems(data) {
  var cartItemsDiv = document.getElementById('cart-items');
  var totalPriceDiv = document.getElementById('total-price');

  cartItemsDiv.innerHTML = '';
  totalPriceDiv.innerHTML = '';

  for (var i = 0; i < data.length - 1; i++) {
    var item = data[i];
    var itemDiv = document.createElement('div');
    itemDiv.classList.add('card','card-'+item.id,'mt-4');
    var cardTitlDiv = document.createElement('div');
    cardTitlDiv.classList.add('card-title','h5');
    cardTitlDiv.textContent = '' + item.product;
    var cardBodyDiv = document.createElement('div');
    cardBodyDiv.classList.add('card-body');
    var itemContent = document.createElement('div');
    itemContent.classList.add('card-text', 'row', 'justify-content-center','align-items-center'); // Add 'align-items-center' class for vertical alignment

    var quantityDiv = document.createElement('div');
    quantityDiv.classList.add('col-12', 'col-md-6');
    quantityDiv.innerHTML = '<strong>العدد:</strong> ' + item.quantity;

    var reduceButton = document.createElement('button');
    reduceButton.classList.add('btn', 'btn-sm', 'btn-danger');
    reduceButton.textContent = '-';
    reduceButton.dataset.itemId = item.id; // Save the item ID as a data attribute
    var addButton = document.createElement('button');
    addButton.classList.add('btn', 'btn-sm', 'btn-success', 'ml-2',);
    addButton.textContent = '+';
    addButton.dataset.itemId = item.id; // Save the item ID as a data attribute

    var priceDiv = document.createElement('div');
    priceDiv.classList.add('col-12', 'col-md-4');
    priceDiv.innerHTML = '<strong>سعر الوحدة:</strong> ' + item.price;

    var totalPriceDiv1 = document.createElement('div');
    totalPriceDiv1.classList.add('col-12', 'col-md-4');
    totalPriceDiv1.innerHTML = '<strong>سعر الكل:</strong> ' + item.total_price;

    itemContent.appendChild(addButton); // Add the add button
    itemContent.appendChild(quantityDiv);
    itemContent.appendChild(reduceButton); // Add the reduce button

    itemContent.appendChild(priceDiv);
    itemContent.appendChild(totalPriceDiv1);
    itemDiv.appendChild(cardTitlDiv);
    cardBodyDiv.appendChild(itemContent);
    itemDiv.appendChild(cardBodyDiv);
    cartItemsDiv.appendChild(itemDiv);
  }

  if (data.length > 0) {
    var totalDiv = document.createElement('div');
    totalDiv.classList.add('card', 'w-50');
    totalDiv.textContent = 'تكلفة الفاتورة: ' + data[data.length - 1].total_price;
    totalPriceDiv.appendChild(totalDiv);
  }

  // Attach event listeners to the reduce and add buttons
  var reduceButtons = document.querySelectorAll('#cart-items button.btn-danger');
  var addButtons = document.querySelectorAll('#cart-items button.btn-success');

  reduceButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      var itemId = button.dataset.itemId;
      console.log(itemId)
      updateCartItemQuantity(itemId, -1,data); // Call a function to update the quantity
    });
  });

  addButtons.forEach(function(button) {
    button.addEventListener('click', function() {
      var itemId = button.dataset.itemId;
      updateCartItemQuantity(itemId, 1,data); // Call a function to update the quantity
    });
  });

}
  });

  
