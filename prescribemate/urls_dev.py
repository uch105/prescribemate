from django.urls import path
from django.http import HttpResponse
from dev import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('dashboard/add-generic-features/', views.add_generic_features, name='addgenericfeatures'),
]