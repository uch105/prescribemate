from django.urls import path
from django.http import HttpResponse
from dev import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutview, name='logout'),
    path('dashboard/add-generic-features/', views.add_generic_features, name='addgenericfeatures'),
]

from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve , {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve , {'document_root': settings.STATIC_ROOT}),
]