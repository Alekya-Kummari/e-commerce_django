from django.urls import path

from AdminApp import views
urlpatterns = [
    path('login', views.login),
    path('AdminAction', views.AdminAction),
    path('addservice', views.addservice),
    path('adminhome', views.AdminHome),
    path('ViewCustomers',views.ViewCustomers),
    path('accept',views.accept),
    path('serviceaction', views.serviceaction),
    path('viewserivces', views.viewserivces),
    path('AddSerivces',views.AddSerivces),
    path('ServiceRegAction',views.ServiceRegAction),
    path('AddProducts',views.AddProducts),
    path('ProductAction',views.ProductAction),
    path('viewproducts',views.viewproducts),
    path('viewbookings',views.viewbookings),
    path('AcceptService',views.AcceptService),
    path('AcceptProduct',views.AcceptProduct),
    path('recommend', views.recommend_products, name='recommend_products'),
]
