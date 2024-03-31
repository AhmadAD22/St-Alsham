from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem, Product
from menu.models import *
from .models import *
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from django.conf import settings
# import os
# from PyPDF2 import PdfMerger

# def generate_order_pdf(order):
#     # Create a new PDF document
#     pdf = canvas.Canvas(f'order_{order.id}.pdf')

#     # Set up the document title
#     pdf.setFont('Helvetica-Bold', 16)
#     pdf.drawString(50, 750, f"Order #{order.id}")

#     # Set up the table information
#     pdf.setFont('Helvetica', 12)
#     pdf.drawString(50, 700, f"Table: {order.table}")
#     pdf.drawString(50, 680, "Items:")

#     # Set up the items table headers
#     pdf.setFont('Helvetica-Bold', 12)
#     pdf.drawString(50, 660, "Product")
#     pdf.drawString(200, 660, "Quantity")
#     pdf.drawString(300, 660, "Price")
#     pdf.drawString(400, 660, "Total")

#     # Set up the items table rows
#     pdf.setFont('Helvetica', 12)
#     y = 640
#     for item in order.orderitem_set.all():
#         pdf.drawString(50, y, str(item.product.name))
#         pdf.drawString(200, y, str(item.quantity))
#         pdf.drawString(300, y, str(item.price))
#         pdf.drawString(400, y, str(item.get_item_total()))
#         y -= 20

#     # Set up the total price
#     pdf.setFont('Helvetica-Bold', 12)
#     pdf.drawString(300, y - 20, "Total Price:")
#     pdf.drawString(400, y - 20, str(order.get_total_price()))

#     # Save the PDF document
#     pdf.save()

# def generate_all_order_pdfs():
#     orders = Order.objects.all()

#     # Generate PDFs for all orders
#     for order in orders:
#         generate_order_pdf(order)

#     # Merge the generated PDFs into a single file
#     merger = PdfMerger()
#     for order in orders:
#         filename = f'order_{order.id}.pdf'
#         merger.append(filename)

#     # Save the merged PDF
#     output_filename = 'all_orders.pdf'
#     merger.write(output_filename)
#     merger.close()

#     # Remove the individual order PDF files
#     for order in orders:
#         filename = f'order_{order.id}.pdf'
#         os.remove(filename)

# # Generate PDFs for all orders and merge them
# generate_all_order_pdfs()

class CartItemQuantityUpdateAPIView(APIView):
    def post(self, request):
        itemId = request.data.get('itemId')
        quantityChange = int(request.data.get('quantityChange'))

        cart_item = get_object_or_404(CartItem, id=itemId)
        cart_item.quantity += quantityChange

        if cart_item.quantity > 0:
            cart_item.save()
            return Response({'message': 'Item updated'}, status=status.HTTP_200_OK)
        else:
            cart_item.delete()
            return Response({'message': 'deleted.'}, status=status.HTTP_200_OK)

class AddToCartAPIView(APIView):
    def post(self, request):
        table_id = request.data.get('table_id')
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            table = Table.objects.get(id=table_id)
            product = Product.objects.get(id=product_id)
        except (Table.DoesNotExist, Product.DoesNotExist):
            return Response(
                {'error': 'Invalid table or product.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(table=table)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return Response({'success': 'Item added to cart.'}, status=status.HTTP_200_OK)
    
class CartItemsAPIView(APIView):
    def get(self, request, cart_id):
        try:
            cart = Cart.objects.get(id=cart_id)
            
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Cart does not exist.'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart_items = CartItem.objects.filter(cart=cart)
        data = []
        total_price = 0  # Variable to store the total price
        for cart_item in cart_items:
            item_data = {
                'id':cart_item.id,
                'product': cart_item.product.name,
                'quantity': cart_item.quantity,
                'price': cart_item.product.price,
            }
            data.append(item_data)
            total_item_price = cart_item.quantity * cart_item.product.price
            item_data['total_price'] = total_item_price
            total_price += total_item_price
        

        # Add the total price to the response data
        data.append({'total_price': total_price})

        return Response(data, status=status.HTTP_200_OK)

class ConfirmOrderAPIView(APIView):
    def post(self, request):
        tableId = request.data.get('tableId')
        try:
            cart = Cart.objects.get(table__id=tableId)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'السلة غير موجودة'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if cart items are empty
        if cart.cartitem_set.count() == 0:
            return Response(
                {'error': 'السلة فارغة'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        # Create a new Order object
        order = Order.objects.create(table=cart.table)

        # Move cart items to the order
        for cart_item in cart.cartitem_set.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        # Clear the cart after confirming the order
        cart.cartitem_set.all().delete()

        return Response({'message': 'تم إرسال الطلب'}, status=status.HTTP_200_OK)


