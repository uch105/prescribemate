from core.models import *
import os
from prescribemate import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django_hosts import reverse as hosts_reverse
from django.http import HttpResponseForbidden
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model

User = get_user_model()

@login_required(login_url='login/')
def home(request):
    return render(request, 'dev/dashboard.html')

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            if username[:3] == 'dev':
                user = authenticate(request, username=username,password=password)
                if user is not None:
                    login(request, user)
                    return redirect(hosts_reverse('home', host='dev'))
                else:
                    return HttpResponseForbidden("Invalid username or password")
            else:
                return HttpResponseForbidden("Wrong user. Warning!")
        except:
            return HttpResponseForbidden("Access Denied! Contact Admin.")
    return render(request, 'dev/login.html')

def logoutview(request):
    logout(request)
    return redirect("login")
'''
JSON_FILE = os.path.join(settings.BASE_DIR, 'core','corefiles','generic_features.json')

def _load_data():
    """Helper to load JSON data."""
    try:
        with open(JSON_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save_data(data):
    """Helper to save data to JSON file."""
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)
'''

@login_required(login_url='login/')
def add_generic_features(request):
    if request.method == "POST":
        generic_name = request.POST.get("generic_name")
        if not generic_name:
            messages.error(request, "Generic name is required")
            return redirect('addgenericfeatures')

        try:
            instance, created = DrugGeneric.objects.get_or_create(
                generic_name=generic_name,
                defaults={
                    'indications_list': request.POST.get("indications_list", ""),
                    'contraindications_list': request.POST.get("contraindications_list", ""),
                    'side_effects_list': request.POST.get("side_effects_list", ""),
                    'theraputic_classes_list': request.POST.get("theraputic_classes_list", ""),
                    'dosage_administrations': request.POST.get("dosage_administrations", ""),
                    'dosage_administrations_list': request.POST.get("dosage_administrations_list", ""),
                    'pregnancy_lactations': request.POST.get("pregnancy_lactations", ""),
                    'interactions': request.POST.get("interactions", ""),
                    'mechanism_of_actions': request.POST.get("mechanism_of_actions", ""),
                    'precautions_warnings': request.POST.get("precautions_warnings", ""),
                    'storage': request.POST.get("storage", ""),
                    'overdose': request.POST.get("overdose", "")
                }
            )

            if not created:
                instance.indications_list = request.POST.get("indications_list", instance.indications_list)
                instance.contraindications_list = request.POST.get("contraindications_list", instance.contraindications_list)
                instance.side_effects_list = request.POST.get("side_effects_list", instance.side_effects_list)
                instance.theraputic_classes_list = request.POST.get("theraputic_classes_list", instance.theraputic_classes_list)
                instance.dosage_administrations = request.POST.get("dosage_administrations", instance.dosage_administrations)
                instance.dosage_administrations_list = request.POST.get("dosage_administrations_list", instance.dosage_administrations_list)
                instance.pregnancy_lactations = request.POST.get("pregnancy_lactations", instance.pregnancy_lactations)
                instance.interactions = request.POST.get("interactions", instance.interactions)
                instance.mechanism_of_actions = request.POST.get("mechanism_of_actions", instance.mechanism_of_actions)
                instance.precautions_warnings = request.POST.get("precautions_warnings", instance.precautions_warnings)
                instance.storage = request.POST.get("storage", instance.storage)
                instance.overdose = request.POST.get("overdose", instance.overdose)
                instance.save()

            messages.success(request, f"Generic <name: {generic_name}> {'created' if created else 'updated'} successfully")
            return redirect('addgenericfeatures')
        
        except Exception as e:
            messages.error(request, f"Error processing request: {str(e)}")
            return redirect('addgenericfeatures')
    
    file_path = os.path.join(
        settings.BASE_DIR,
        'core', 
        'corefiles', 
        'generic_names.txt'
    )
    try:
        generic_list = []
        with open(file_path, 'r') as file:
            for line in file:
                generic_list.append(line.strip())
    except FileNotFoundError:
        generic_list = []
    
    context = {
        'generic_list': generic_list,
    }
    return render(request, 'dev/add_generic_features.html', context)