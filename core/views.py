import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prescribemate.settings')
django.setup()

from django.shortcuts import render,redirect,HttpResponse
from .models import *
from common.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
import random
import string

User = get_user_model()

def generate_unique_id(prefix="id_", length=16, include_uppercase=True, include_lowercase=True, include_numbers=True, include_special=True):
    if length <= len(prefix):
        raise ValueError("Length must be greater than prefix length.")

    characters = ""

    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character set must be included.")

    remaining_length = length - len(prefix)
    random_part = ''.join(random.choice(characters) for _ in range(remaining_length))

    return prefix + random_part

def generate_username(prefix):
    while True:
        username = generate_unique_id(prefix=prefix, include_special=False)
        if not User.objects.filter(username=username).exists():
            return username

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def pricing(request):
    return HttpResponse("Pricing page is under construction.")

def blogs(request):
    return HttpResponse("Blogs page is under construction.")

def contact(request):
    return HttpResponse("Contact page is under construction.")

def about(request):
    return HttpResponse("About page is under construction.")

def careers(request):
    return HttpResponse("Careers page is under construction.")

def press(request):
    return HttpResponse("Press page is under construction.")

def api_docs(request):
    return HttpResponse("API Documentation page is under construction.")

def home(request):
    return render(request, 'core/landing.html')

@login_required(login_url='/behind-the-desk/login/')
def administration(request):
    hrequests = HospitalRegistrationRequest.objects.all()

    context = {
        'hrequests': hrequests,
    }
    return render(request, 'core/administration.html', context)

@login_required(login_url='/behind-the-desk/login/')
def hospitalregistrationrequestapprove(request, pk):
    try:
        hospital = HospitalRegistrationRequest.objects.get(id=pk)
        new_hospital = Hospital.objects.filter(reg_code=hospital.reg_code).first()
        
        if not new_hospital:
            messages.error(request, "Matching hospital not found")
            return redirect('administration')

        new_hospital.legal_contact = hospital.legal_contact
        new_hospital.verified = True

        if hospital.logo:
            if new_hospital.logo:
                new_hospital.logo.close()
                new_hospital.logo.delete(save=False)

            new_hospital.logo = hospital.logo
            hospital.logo = None
        
        new_hospital.save()
        
        HospitalWallet.objects.create(
            hospital=new_hospital,
            balance=0.0,
        )

        username = f"admin-{new_hospital.reg_code}"
        password = make_password(hospital.password)

        User.objects.create(username=username, role=User.Roles.HOSPITAL_ADMIN, name=f"Admin - {new_hospital.brand_name}", password=password)
        
        HospitalEmployee.objects.create(
            user=User.objects.get(username=username),
            hospital=new_hospital,
            role = User.objects.get(username=username).role,
        )

        hospital.delete()
        
        messages.success(request, "Hospital verified successfully")
    
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
    
    return redirect('administration')