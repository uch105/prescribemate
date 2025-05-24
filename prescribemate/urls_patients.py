from django.urls import path
from django.http import HttpResponse

def patient_home(request):
    return HttpResponse("Patients Subdomain: Hello Patient!")

urlpatterns = [
    path('', patient_home),
]
