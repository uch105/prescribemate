import string,random

# ========== CORE FUNCTIONS =============

def generate_unique_id(prefix="id_", length=20, include_uppercase=True, include_lowercase=True, include_numbers=True, include_special=True):
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

def get_districts_list():
    districts = []
    with open('/home/uch/prescribemate/core/corefiles/districts.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            districts.append(line.strip('\n'))
    return districts

def get_sub_districts_list():
    sub_districts = []
    with open('/home/uch/prescribemate/core/corefiles/sub_districts.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            sub_districts.append(line.strip('\n'))
    return sub_districts

# ==================== VIEW FUNCTIONS =====================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from common.models import *
from core.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
'''
if not request.user.check_password(old_password):

# Change password
request.user.set_password(new_password)
request.user.save()

# Keep the user logged in
update_session_auth_hash(request, request.user)
'''

User = get_user_model()


def landing_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        reg_code = request.POST.get('reg_code')
        phone = request.POST.get('phone')
        district = request.POST.get('district')
        sub_district = request.POST.get('sub_district')
        password = request.POST.get('password')
        logo = request.FILES['logo']

        HospitalRegistrationRequest.objects.create(
            brand_name=name,
            reg_code=reg_code,
            legal_contact=phone,
            district=district,
            upazilla=sub_district,
            password=password,
            logo=logo,
        )

        messages.success(request, "Request sent. An admin will review it soon.")

        return redirect('hospital_landing')

    context = {
        'districts': get_districts_list(),
        'upazillas': get_sub_districts_list(),
    }
    return render(request, 'hospitals/landing.html',context)

def hospital_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.role in [User.Roles.HOSPITAL_ADMIN, User.Roles.HOSPITAL_ACCOUNTANT, User.Roles.HOSPITAL_EMERGENCY, User.Roles.HOSPITAL_EMPLOYEE, User.Roles.HOSPITAL_NURSE, User.Roles.HOSPITAL_PHARMACY, User.Roles.HOSPITAL_RECEIPTION]:
            login(request, user)
            return redirect('hospital_dashboard')
        else:
            return render(request, 'hospitals/login.html', {'error': 'Invalid credentials'})
        
    if request.user.is_authenticated:
        return redirect('hospital_dashboard')
    
    return render(request, 'hospitals/login.html')

def hospital_logout(request):
    logout(request)
    return redirect('hospital_login')

@login_required(login_url='/login/')
def hospital_dashboard(request):
    if not request.user.role.startswith(User.Roles.HOSPITAL_ADMIN):
        messages.error(request, "You do not have permission to access this page.")
        context = {
            'error': "You do not have permission to access this page."
        }
    else:
        user = HospitalEmployee.objects.get(user=request.user)
        hospital = user.hospital
        total_pharmacy = HospitalPharmacy.objects.filter(reg_code=hospital.reg_code).count()
        wallet = HospitalWallet.objects.filter(hospital=hospital).first()
        total_employee = HospitalEmployee.objects.filter(hospital=hospital).count()
        total_ward = HospitalWard.objects.filter(hospital=user.hospital).count()
        total_bed = HospitalWardBed.objects.filter(hospital=user.hospital).count()
        context = {
            'user': user,
        }
    return render(request, 'hospitals/dashboard.html',context)