from django.urls import path
from django.http import HttpResponse

def pharmacy_home(request):
    return HttpResponse("Pharmacy Subdomain: Hello Pharmacy!")

urlpatterns = [
    path('', pharmacy_home),
]
