from django.urls import path

from Customer import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('Register', views.Register),
    path('RegAction', views.RegAction),
    path('LogAction', views.LogAction),
    path('CustomerHome', views.CustomerHome),
    path('ViewService', views.ViewService),
    path('BookService', views.BookService),
    path('ViewProducts', views.ViewProducts),
    path('CartProduct',views.CartProduct),
    path('ViewCart',views.ViewCart),
    path('CartAction',views.CartAction),
    path('BookProduct', views.BookProduct),
    path('viewbookings', views.viewbookings),
    path('recommend', views.customer_recommendation, name='customer_recommendation'),
]
