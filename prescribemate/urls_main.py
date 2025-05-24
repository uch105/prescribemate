from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("Main site: Welcome to PrescribeMate!")

urlpatterns = [
    path('', home),
]
