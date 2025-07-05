from django.urls import path
from django.http import HttpResponse
from core import views
from django.contrib import admin

def home(request):
    return HttpResponse("Main site: Welcome to PrescribeMate!")

urlpatterns = [
    path('', home, name='home'),
    path('behind-the-desk/',admin.site.urls),
    path('administration/',views.administration, name="administration"),
    path('sitetraffic/',views.sitetraffic, name="sitetraffic"),
    path('lookup/',views.lookup, name="lookup"),
    path('terms-and-conditions/',views.terms, name="terms"),
    path('privacy-policy/',views.privacy, name="privacy"),
]
