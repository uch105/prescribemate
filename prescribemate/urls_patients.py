from django.urls import path
from django.http import HttpResponse

def patient_home(request):
    return HttpResponse("Patients Subdomain: Hello Patient!")

urlpatterns = [
    path('', patient_home),
]

from django.urls import re_path
from django.conf import settings
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve , {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve , {'document_root': settings.STATIC_ROOT}),
]