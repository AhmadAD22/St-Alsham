from django.urls import path
from .views import *

urlpatterns = [
    path('',main_dashboard,name="main_dashboard"),
    #Orders
    path('new_orders',new_orders,name="new_orders"),
    path('order/<int:order_id>', order_details, name='dashboard_order_details'),
    path('orders/perform/<int:order_id>', performe_order, name='perform_orders'),
    path('orders/performed', performed_orders, name='performed_orders'),
    path('orders/not_collected', not_collected_orders, name='not_collected'),
    path('orders/collect', collect_orders, name='collect_orders'),
    #Products
    path('product/create/', create_product, name='create_product'),
    path('product/update/<int:pk>/', update_product, name='update_product'),
    path('product/delete/<int:pk>/', delete_product, name='delete_product'),
    path('product/list/', product_list, name='product_list'),
    #Category
    path('category_list',category_list,name="category_list"),
    path('delete_category/<int:pk>',delete_category,name="delete_category"),
    path('create_category',create_category,name="create_category"),
    path('category/edit/<int:pk>/', edit_category, name='edit_category'),
    #users
    path('user_list',user_list,name="user_list"),
    path('create_user',create_user,name="create_user"),
    path('update_user/<int:pk>',update_user,name="update_user"),
    path('delete_user/<int:pk>',delete_user,name="delete_user"),
    
    path('login/',login_user, name='login'),
    path('logout/',logout_user, name='logout'),
     
]
