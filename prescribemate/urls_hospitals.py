from django.urls import path
from hospitals import views

urlpatterns = [
    path('', views.landing_page, name='hospital_landing'),
    path('login/', views.hospital_login, name='hospital_login'),
    path('logout/', views.hospital_logout, name='hospital_logout'),
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
]

from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve , {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve , {'document_root': settings.STATIC_ROOT}),
]