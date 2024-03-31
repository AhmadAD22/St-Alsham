from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('<int:table_num>',menu,name="menu"),
]

