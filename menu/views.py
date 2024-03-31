from django.shortcuts import render
from django.conf import settings
from .models import *

def menu (request,table_num):
    table=Table.objects.get(table_number=table_num)
    products=Product.objects.all()
    categories=Category.objects.all()
    context={
        'products':products,
        'table_num':table_num,
        'categories':categories,
    }
    return render(request,'menu.html',context)
