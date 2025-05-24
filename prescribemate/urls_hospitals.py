from django.urls import path
from django.http import HttpResponse

def hospital_home(request):
    return HttpResponse("Hospitals Subdomain: Hello Hospital!")

urlpatterns = [
    path('', hospital_home),
]
