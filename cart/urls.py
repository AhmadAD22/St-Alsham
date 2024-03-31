from django.urls import path
from .views import *

urlpatterns = [
path('api/add-to-cart/', AddToCartAPIView.as_view(), name='add_to_cart_api'),
path('api/cart-items/<int:cart_id>/', CartItemsAPIView.as_view(), name='cart_items_api'),
path('update-cart-item-quantity/', CartItemQuantityUpdateAPIView.as_view(), name='update_cart_item_quantity'),
path('confirm-order/', ConfirmOrderAPIView.as_view(), name='confirm_order'),


]