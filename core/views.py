import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prescribemate.settings')
django.setup()

from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
import random
import string

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Logged In successfully')
            next_url = request.POST.get('next', '/')
            return redirect(next_url)
        else:
            messages.add_message(request, messages.ERROR, "Username and/or password didn't match")
            return redirect('login')

    next_url = request.GET.get('next', '')
    return render(request, 'core/login.html', {'next': next_url})

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out successfully')
    return redirect('home')

@login_required
def doctor_as_dev(request):
    if request.method == "POST":
        generic = request.POST.get("generic")
        indication = request.POST.get("indication")
        contraindication = request.POST.get("contraindication")
        side_effect = request.POST.get("side_effect")

        drugs = Drug.objects.filter(generic=generic)
        for drug in drugs:
            drug.indication = indication
            drug.contraindication = contraindication
            drug.side_effect = side_effect
        
        messages.add_message(request,messages.INFO, f"Properties for {generic} added successfully!")
        return redirect('index')
        

    with open('/home/uch/prescribemate/core/corefiles/generic_names.xlsx','r') as file:
        lines = [line for line in file]
        generics = [line.rstrip('\n') for line in lines]
    context = {
        'generics': generics,
    }
    return render(request,'core/doctor_as_dev.html',context)

def terms(request):
    return render(request, 'core/terms.html')

def privacy(request):
    return render(request, 'core/privacy.html')

@login_required
def sitetraffic(request):
    context = {}
    return render(request, 'core/sitetraffic.html', context)

@login_required
def administration(request):
    if request.method == "POST":
        role = request.POST.get('role','')
        name = request.POST.get('name','')

    context = {}
    return render(request, 'core/administration.html', context)

@login_required
def lookup(request):
    context = {}
    return render(request, 'core/lookup.html', context)