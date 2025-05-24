from django.urls import path
from django.http import HttpResponse

def doctor_home(request):
    return HttpResponse("Doctors Subdomain: Hello Doctor!")

urlpatterns = [
    path('', doctor_home),
]
