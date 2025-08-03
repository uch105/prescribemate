from django.urls import path
from django.http import HttpResponse
from core import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('behind-the-desk/',admin.site.urls),
    path('terms-and-conditions/',views.terms, name="terms"),
    path('privacy-policy/',views.privacy, name="privacy"),
    path('pricing/',views.pricing, name="pricing"),
    path('about-us/',views.about, name="about"),
    path('contact-us/',views.contact, name="contact"),
    path('press/',views.press, name="press"),
    path('careers/',views.careers, name="careers"),
    path('blogs/',views.blogs, name="blogs"),
    path('api-docs/',views.api_docs, name="api_docs"),
    path('administration/',views.administration, name="administration"),
    path('hospitalregistrationrequestapprove/<int:pk>/',views.hospitalregistrationrequestapprove, name="hospitalregistrationrequestapprove"),
]

from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve , {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve , {'document_root': settings.STATIC_ROOT}),
]