from django.urls import path
from . import views

urlpatterns = [
    path('',views.login, name = "Login"),
    path('home/',views.index, name = "index"),
    path('add/',views.add, name = "add"),
    path('delete/',views.delete, name = "delete"),
    
]