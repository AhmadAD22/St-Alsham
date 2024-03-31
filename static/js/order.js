
$(document).ready(function() {
    $('#confirm-button').click(function() {
      var tableId = document.getElementById('table-id-input').value;
  
      $.ajax({
        url: 'http://127.0.0.1:8000/cart/confirm-order/',
        type: 'POST',
        data: { tableId: tableId },
        success: function(response) {
          // Handle the successful response here
          // Append success message to the alert container
          var successAlert = $('<div class="alert alert-success">' + response.message + '</div>');
          $('#alert-container').html(successAlert);
             // Store the success message in local storage
          // Hide the alert after 3 seconds
          setTimeout(function() {
            successAlert.fadeOut('slow');
          }, 1000);
          // Clear the cart items from the DOM
          var cartItemsDiv = document.getElementById('cart-items');
          cartItemsDiv.innerHTML = '';
          
          
        },
        error: function(xhr, textStatus, errorThrown) {
          // Handle any errors here
          // Append error message to the alert container
          var errorAlert = $('<div class="alert alert-danger">' + xhr.responseJSON.error + '</div>');
          $('#alert-container').html(errorAlert);
         
          // Hide the alert after 3 seconds
          setTimeout(function() {
            errorAlert.fadeOut('slow');
          }, 1000);
        }
      });
    });
  });