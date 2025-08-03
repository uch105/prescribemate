# ---------------- common/models.py ------------------

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from django.utils import timezone
from datetime import timedelta
from datetime import date
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError(_('The Username must be set'))
        
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a staff user with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Staff user must have is_staff=True.'))
        
        return self.create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given username and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        PATIENT = 'patient', _('Patient')
        DOCTOR = 'doctor', _('Doctor')
        INTERN_DOCTOR = 'intern_doctor', _('Intern Doctor')
        ADMIN = 'admin', _('Admin')
        PHARMACY = 'pharmacy', _('Pharmacy')
        HOSPITAL = 'hospital', _('Hospital')
        DIAGNOSTIC = 'hospital_diagnostic', _('Hospital Diagnostic')
        DUTY_DOCTOR = 'duty_doctor', _('Duty Doctor')
        OUTDOOR_DOCTOR = 'outdoor_doctor', _('Outdoor Doctor')
        HOSPITAL_EMPLOYEE = 'hospital_employee', _('Hospital Employee')
        HOSPITAL_PHARMACY = 'hospital_pharmacy', _('Hospital Pharmacy')
        HOSPITAL_ACCOUNTANT = 'hospital_accountant', _('Hospital Accountant')
        HOSPITAL_RECEIPTION = 'hospital_receiption', _('Hospital Receiption')
        HOSPITAL_ADMIN = 'hospital_admin', _('Hospital Admin')
        HOSPITAL_NURSE = 'hospital_nurse', _('Hospital Nurse')
        HOSPITAL_EMERGENCY = 'hospital_emergency', _('Hospital Emergency')

    username = models.CharField(
        max_length=150,
        unique=True,
        db_index=True # Keep db_index=True as it's unique
    )
    
    name = models.CharField(_('full name'), max_length=255, blank=True) # db_index=True removed
    
    role = models.CharField(
        _('role'),
        max_length=30,
        choices=Roles.choices,
        default=Roles.PATIENT
    ) # db_index=True removed
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
        db_index=True # Keep db_index=True for boolean filters
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
        db_index=True # Keep db_index=True for boolean filters
    )
    
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True) # db_index=True removed
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['username']
        indexes = [
            models.Index(fields=['name']), # For queries filtering only by name
            models.Index(fields=['role']), # For queries filtering only by role
            models.Index(fields=['date_joined']), # For queries filtering only by date_joined
            models.Index(fields=['username', 'role']), # Common lookup by username and role
            models.Index(fields=['name', 'role']), # Common lookup by name and role
            models.Index(fields=['role', 'is_active']), # Filter by role and active status
            models.Index(fields=['-date_joined']), # For getting most recent users
        ]

    def __str__(self):
        return f"{self.name or self.username} ({self.get_role_display()})"

    def get_full_name(self):
        return self.name
    
    def get_role_display(self):
        return self.role

    def get_short_name(self):
        return self.name.split()[0] if self.name else self.username

def user_test_result_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/test_<id>/<filename>
    return f'user_{instance.user.username}/test_{instance.test.testID}/{filename}'

def user_media_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.username}/{filename}'

class FamilyMember(models.Model):

    class Relations(models.TextChoices):
        FATHER = 'father', _('Father')
        MOTHER = 'mother', _('Mother')
        BROTHER = 'brother', _('Brother')
        SISTER = 'sister', _('Sister')
        HUSBAND = 'husband', _('Husband')
        WIFE = 'wife', _('Wife')
        F_COUSIN = 'fathersidecousin', _('Father Side Cousin')
        M_COUSIN = 'mothersidecousin', _('Mother Side Cousin')
        IN_LAWS = 'inlaws', _('In Laws')
        OTHERS = 'others', _('Otehrs')

    username1 = models.OneToOneField(User, on_delete=models.CASCADE,related_name="main_member") # db_index=True removed
    username2 = models.OneToOneField(User, on_delete=models.CASCADE,related_name="related_member") # db_index=True removed
    relation = models.CharField(
        _('relation'), 
        max_length=30,
        choices=Relations.choices,
        default=Relations.OTHERS
        ) # Keep db_index=True for single field

    class Meta:
        verbose_name_plural = "Family Members"
        ordering = ['username1__username', 'username2__username']
        indexes = [
            models.Index(fields=['username1']), # For queries filtering only by username1
            models.Index(fields=['username2']), # For queries filtering only by username2
            models.Index(fields=['username1', 'username2']), # Index for finding relationships
            models.Index(fields=['username1', 'relation']), # Index for finding relations of a user
            models.Index(fields=['username2', 'relation']), # Index for finding relations where username2 is the main
        ]

    def __str__(self):
        return f"{self.username1} is {self.relation} of {self.username2}"

class BloodDonor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # db_index=True removed
    donated = models.IntegerField(default=0)
    last_donated = models.DateField() # db_index=True removed
    area = models.TextField(null=True,blank=True) # db_index=True removed

    class Meta:
        verbose_name_plural = "Blood Donors"
        ordering = ['user__name', '-last_donated']
        indexes = [
            models.Index(fields=['user']), # For queries filtering only by user
            models.Index(fields=['last_donated']), # For queries filtering only by last_donated
            models.Index(fields=['area']), # For queries filtering only by area
            models.Index(fields=['area', 'last_donated']), # Search donors by area and last donation date
            models.Index(fields=['last_donated', 'area']), # Search donors by last donation date and area
        ]

    def __str__(self):
        return f"{self.user.name} -- {self.area} -- {self.last_donated}"
        
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # db_index=True removed
    nid = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    brn = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    name = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    phone = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    sex = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    bg = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    religion = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=user_media_path, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Patients"
        ordering = ['name', 'phone']
        indexes = [
            models.Index(fields=['name']), # For queries filtering only by name
            models.Index(fields=['phone']), # For queries filtering only by phone
            models.Index(fields=['nid']), # For queries filtering only by NID
            models.Index(fields=['brn']), # For queries filtering only by BRN
            models.Index(fields=['sex']), # For queries filtering only by sex
            models.Index(fields=['bg']), # For queries filtering only by blood group
            models.Index(fields=['name', 'phone']), # Common search by name and phone
            models.Index(fields=['sex', 'bg']), # Filter patients by sex and blood group
            models.Index(fields=['name', 'sex']), # Filter by name and sex
            models.Index(fields=['phone', 'nid']), # Filter by phone and NID
        ]

    def __str__(self):
        return f"{self.name} - {self.phone} - {self.address}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # db_index=True removed
    nid = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    brn = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    name = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    phone = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    sex = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    bg = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    religion = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=user_media_path, null=True, blank=True)
    bmdc = models.CharField(max_length=255, unique=True, null=False, default='Duty Doctor', db_index=True) # Keep db_index=True as it's unique
    qualifications = models.TextField(null=True, blank=True)
    job_location = models.TextField(null=True, blank=True) # db_index=True removed
    verified = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters

    class Meta:
        verbose_name_plural = "Doctors"
        ordering = ['name', 'bmdc']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone']),
            models.Index(fields=['nid']), # For queries filtering only by NID
            models.Index(fields=['brn']), # For queries filtering only by BRN
            models.Index(fields=['sex']), # For queries filtering only by sex
            models.Index(fields=['bg']), # For queries filtering only by blood group
            models.Index(fields=['name', 'phone']), # Common search by name and phone
            models.Index(fields=['sex', 'bg']), # Filter patients by sex and blood group
            models.Index(fields=['name', 'sex']), # Filter by name and sex
            models.Index(fields=['phone', 'nid']), # Filter by phone and NID
            models.Index(fields=['job_location']),
            models.Index(fields=['name', 'job_location']), # Search doctors by name and location
            models.Index(fields=['verified', 'job_location']), # Filter verified doctors by location
            models.Index(fields=['sex', 'job_location']), # Filter by sex and job location
            models.Index(fields=['name', 'verified']), # Filter by name and verification status
        ]

    def __str__(self):
        return f"{self.name} - {self.bmdc} - {self.address}"
    
class Pharmacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # db_index=True removed
    nid = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    brn = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    name = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    phone = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    sex = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    bg = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    religion = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to=user_media_path, null=True, blank=True)
    trade_lic = models.CharField(max_length=255, unique=True, null=False, default='Duty Doctor', db_index=True) # Keep db_index=True as it's unique
    pharmacy_image = models.ImageField(upload_to=user_media_path,null=False)
    pharmacy_location = models.TextField(null=True, blank=True) # db_index=True removed
    verified = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters

    class Meta:
        verbose_name_plural = "Pharmacies"
        ordering = ['name', 'trade_lic']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['phone']),
            models.Index(fields=['nid']), # For queries filtering only by NID
            models.Index(fields=['brn']), # For queries filtering only by BRN
            models.Index(fields=['sex']), # For queries filtering only by sex
            models.Index(fields=['bg']), # For queries filtering only by blood group
            models.Index(fields=['name', 'phone']), # Common search by name and phone
            models.Index(fields=['sex', 'bg']), # Filter patients by sex and blood group
            models.Index(fields=['name', 'sex']), # Filter by name and sex
            models.Index(fields=['phone', 'nid']), # Filter by phone and NID
            models.Index(fields=['pharmacy_location']),
            models.Index(fields=['pharmacy_location', 'verified']), # Filter pharmacies by location and verification
            models.Index(fields=['name', 'pharmacy_location']), # Filter by name and location
        ]

    def __str__(self):
        return f"{self.name} - {self.phone} - {self.address}"

class Hospital(models.Model):
    brand_name = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    reg_code = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    facility_type = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    category = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    district = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    upazilla = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    address = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    joining_date = models.DateTimeField(auto_now_add=True) # db_index=True removed
    legal_contact = models.CharField(max_length=255, null=True)
    logo = models.ImageField(upload_to='hospital_images/')
    
    class Meta:
        verbose_name_plural = "Hospitals"
        ordering = ['brand_name', 'district']
        indexes = [
            models.Index(fields=['brand_name']),
            models.Index(fields=['reg_code']),
            models.Index(fields=['district']),
            models.Index(fields=['upazilla']),
            models.Index(fields=['facility_type']),
            models.Index(fields=['category']),
            models.Index(fields=['district', 'upazilla']), # Search hospitals by location
            models.Index(fields=['verified', 'facility_type']), # Filter by verification and type
            models.Index(fields=['brand_name', 'district', 'upazilla']), # Comprehensive location search
            models.Index(fields=['facility_type', 'category', 'district']), # Filter by type, category, and district
        ]

    def __str__(self):
        status = "Verified" if self.verified else "Not Verified"
        return f"{self.brand_name} - from {self.district} - Status {status}"

class HospitalPharmacy(models.Model):
    brand_name = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    reg_code = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    facility_type = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    category = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    district = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    upazilla = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    address = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    joining_date = models.DateTimeField(auto_now_add=True) # db_index=True removed
    legal_contact = models.CharField(max_length=255, null=True)
    logo = models.ImageField(upload_to='hospital_images/')

    class Meta:
        verbose_name_plural = "Hospital Pharmacies"
        ordering = ['brand_name', 'district']
        indexes = [
            models.Index(fields=['brand_name']),
            models.Index(fields=['district']),
            models.Index(fields=['upazilla']),
            models.Index(fields=['district', 'upazilla']),
            models.Index(fields=['verified', 'brand_name']),
            models.Index(fields=['brand_name', 'district']),
            models.Index(fields=['brand_name', 'district', 'upazilla']),
        ]

    def __str__(self):
        return f"{self.brand_name} - {self.upazilla}"

class HospitalEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # db_index=True removed
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='branchemployees') # db_index=True removed
    role = models.CharField(max_length=255, default='Regular') # db_index=True removed
    security_id = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    cv_file = models.FileField(
        upload_to=user_media_path,
        #validators=validate_file_extension,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Hospital Employees"
        ordering = ['user__name', 'hospital__brand_name']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['hospital']),
            models.Index(fields=['role']),
            models.Index(fields=['security_id']),
            models.Index(fields=['hospital', 'role']), # Find employees by hospital and role
            models.Index(fields=['user', 'hospital']), # Find employee by user and hospital
            models.Index(fields=['role', 'security_id']), # Filter by role and security ID
        ]

    def __str__(self):
        return f"{self.user.name} -- {self.role} -- {self.hospital.brand_name}"

class HospitalWard(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='wards') # db_index=True removed
    ward = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed

    class Meta:
        verbose_name_plural = "Hospital Wards"
        ordering = ['hospital__brand_name', 'ward']
        indexes = [
            models.Index(fields=['hospital']),
            models.Index(fields=['ward']),
            models.Index(fields=['hospital', 'ward']), # Find specific ward in a hospital
        ]

    def __str__(self):
        return f"{self.hospital.brand_name} -- {self.ward}"
    
class HospitalWardBed(models.Model):
    class Beds(models.TextChoices):
        GENERAL = 'general', _('General')
        CABIN = 'cabin', _('Cabin')
        PAYING = 'paying', _('Paying')
        ICU = 'icu', _('ICU')
        NICU = 'nicu', _('NICU')
        PICU = 'picu', _('PICU')
        SICU = 'sicu', _('SICU')
        NEURO_ICU = 'neuro_icu', _('Neuro ICU')
        HDU = 'hdu', _('HDU')
        CCU = 'ccu', _('CCU')
        DIALYSIS_UNIT = 'dialysis_unit', _('Dialysis Unit')
        POST_OPERATIVE = 'post_operative', _('Post Operative')
        PAEDIATRIC = 'pediatric', _('Pediatric')
        LABOR_EMERGENCY = 'labor_emergency', _('Labor Emergency')
        CASUALTY = 'casualty', _('Casualty')
        OT = 'ot', _('OT')
        SCANU = 'scanu', _('ScanU')
        BURN_UNIT = 'burn_unit', _('Burn Unit')
        ELETRICAL = 'electrical', _('Electrical')
        SEMI_ELECTRICAL = 'semi_electrical', _('Semi Electrical')
        CHEMOTHERAPY_INFUSION = 'chemotherapy_infusion', _('Chemotherapy Infusion')
        DONOR = 'donor', _('Donor')
        OTHERS = 'others', _('Others')
        
    ward = models.ForeignKey(HospitalWard, on_delete=models.CASCADE, related_name='wardbeds') # db_index=True removed
    bed_type = models.CharField(_('bed'),max_length=255, choices=Beds.choices, default=Beds.GENERAL) # db_index=True removed
    bed_price = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True, db_index=True) # Keep db_index=True for boolean filters
    current_patient = models.ForeignKey(
        Patient,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='occupied_beds'
    ) # db_index=True removed

    class Meta:
        verbose_name_plural = "Hospital Ward Beds"
        ordering = ['ward__hospital__brand_name', 'ward__ward', 'bed_type']
        indexes = [
            models.Index(fields=['ward']),
            models.Index(fields=['bed_type']),
            models.Index(fields=['current_patient']),
            models.Index(fields=['ward', 'is_available']), # Find available beds in a ward
            models.Index(fields=['ward', 'bed_type']), # Find beds of a specific type in a ward
            models.Index(fields=['is_available', 'bed_type']), # Find available beds of a specific type
        ]

    def __str__(self):
        return f"{self.ward.hospital.brand_name} -- {self.ward.ward} -- {self.bed_type}"

class Diagnostic(models.Model):
    brand_name = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    reg_code = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    facility_type = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    category = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    district = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    upazilla = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    address = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    joining_date = models.DateTimeField(auto_now_add=True) # db_index=True removed
    legal_contact = models.CharField(max_length=255, null=True)
    logo = models.ImageField(upload_to='diagnostic_images/')

    class Meta:
        verbose_name_plural = "Diagnostics"
        ordering = ['brand_name', 'district']
        indexes = [
            models.Index(fields=['brand_name']),
            models.Index(fields=['reg_code']),
            models.Index(fields=['district']),
            models.Index(fields=['upazilla']),
            models.Index(fields=['facility_type']),
            models.Index(fields=['category']),
            models.Index(fields=['district', 'upazilla']),
            models.Index(fields=['verified', 'facility_type']),
            models.Index(fields=['brand_name', 'district', 'upazilla']),
            models.Index(fields=['facility_type', 'category', 'district']),
        ]

    def __str__(self):
        status = "Verified" if self.verified else "Not Verified"
        return f"{self.brand_name} - from {self.district} - Status {status}"

class DiagnosticEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # db_index=True removed
    hospital = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, related_name='diagnosticemployees') # db_index=True removed
    role = models.CharField(max_length=255, default='Regular') # db_index=True removed
    security_id = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    cv_file = models.FileField(
        upload_to=user_media_path,
        #validators=validate_file_extension,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Diagnostic Employees"
        ordering = ['user__name', 'hospital__brand_name']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['hospital']),
            models.Index(fields=['role']),
            models.Index(fields=['security_id']),
            models.Index(fields=['hospital', 'role']),
            models.Index(fields=['user', 'hospital']),
            models.Index(fields=['role', 'security_id']),
        ]

    def __str__(self):
        return f"{self.user.name} -- {self.role} -- {self.hospital.brand_name}"

class DiagnosticTest(models.Model):
    testID = models.CharField(max_length=255, primary_key=True)
    hospital_branch = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, related_name='diagnostictests') # db_index=True removed
    test_name  =  models.TextField(null=True, blank=True) # db_index=True removed
    price = models.IntegerField(default=0)
    daily_limit = models.IntegerField(default=0)
    current_usage = models.IntegerField(default=0)
    last_reset_date = models.DateField(auto_now_add=True) # db_index=True removed
    
    class Meta:
        verbose_name_plural = "Diagnostic Tests"
        ordering = ['test_name', 'hospital_branch__brand_name']
        indexes = [
            models.Index(fields=['hospital_branch']),
            models.Index(fields=['test_name']),
            models.Index(fields=['last_reset_date']),
            models.Index(fields=['hospital_branch', 'test_name']), # Find tests offered by a branch
            models.Index(fields=['test_name', 'price']), # Search tests by name and price
            models.Index(fields=['hospital_branch', 'last_reset_date']), # Filter tests by branch and reset date
        ]

    def reset_daily_limit(self):
        """Reset the usage counter if it's a new day"""
        today = date.today()
        if self.last_reset_date < today:
            self.current_usage = 0
            self.last_reset_date = today
            self.save()
    
    def can_perform_test(self):
        """Check if test can be performed within daily limit"""
        self.reset_daily_limit()
        return self.current_usage < self.daily_limit
    
    def record_test_usage(self):
        """Record a test usage"""
        if self.can_perform_test():
            self.current_usage += 1
            self.save()
            return True
        return False
    
    def __str__(self):
        return f"{self.test_name} ({self.current_usage}/{self.daily_limit})"

class DiagnosticTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userdiagnostictests') # db_index=True removed
    test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE, related_name='diagnostictestresults') # db_index=True removed
    creation_date = models.DateTimeField(auto_now_add=True) # db_index=True removed
    updated_date = models.DateTimeField(auto_now=True)
    result = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to=user_test_result_path, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Diagnostic Test Results"
        ordering = ['-creation_date', 'user__username', 'test__test_name']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['test']),
            models.Index(fields=['creation_date']),
            models.Index(fields=['user', 'test']), # Find a user's result for a specific test
            models.Index(fields=['user', '-creation_date']), # Get a user's most recent results
            models.Index(fields=['test', '-creation_date']), # Get most recent results for a specific test
        ]

    def __str__(self):
        return f"{self.user.username}'s {self.test.test_name} result"
    
class HospitalCoupon(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE, related_name='hospitalscoupons') # db_index=True removed
    coupon_name = models.CharField(max_length=255, null=True,blank=True) # db_index=True removed
    off_amount = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Hospital Coupons"
        ordering = ['hospital__brand_name', 'coupon_name']
        indexes = [
            models.Index(fields=['hospital']),
            models.Index(fields=['coupon_name']),
            models.Index(fields=['hospital', 'coupon_name']), # Find coupons for a hospital by name
        ]

    def __str__(self):
        return f"({self.hospital.brand_name}) -- {self.coupon_name} -- {self.off_amount}"
    
class DiagnosticCoupon(models.Model):
    hospital = models.ForeignKey(Diagnostic,on_delete=models.CASCADE, related_name='diagnosticcoupons') # db_index=True removed
    coupon_name = models.CharField(max_length=255, null=True,blank=True) # db_index=True removed
    off_amount = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Diagnostic Coupons"
        ordering = ['hospital__brand_name', 'coupon_name']
        indexes = [
            models.Index(fields=['hospital']),
            models.Index(fields=['coupon_name']),
            models.Index(fields=['hospital', 'coupon_name']),
        ]

    def __str__(self):
        return f"({self.hospital.brand_name}) -- {self.coupon_name} -- {self.off_amount}"
    
class HospitalAdmission(models.Model):
    branch = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospitalpatients') # db_index=True removed
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admitted_hospitals') # db_index=True removed
    admissioninfo =  models.TextField(null=True, blank=True)
    admission_time = models.DateTimeField(auto_now_add=True) # db_index=True removed
    left = models.BooleanField(default=False)
    leave_time = models.DateTimeField(auto_now=True) # db_index=True removed

    class Meta:
        verbose_name_plural = "Hospital Admissions"
        ordering = ['-admission_time', 'patient__name', 'branch__brand_name']
        indexes = [
            models.Index(fields=['branch']),
            models.Index(fields=['patient']),
            models.Index(fields=['admission_time']),
            models.Index(fields=['leave_time']),
            models.Index(fields=['patient', '-admission_time']), # Get a patient's most recent admissions
            models.Index(fields=['patient', 'left']), # Get a patient has left or not
            models.Index(fields=['branch', '-admission_time']), # Get recent admissions for a hospital
            models.Index(fields=['branch', 'patient']), # Check if a patient was admitted to a specific branch
            models.Index(fields=['admission_time', 'leave_time']), # For time range queries
        ]

    def __str__(self):
        return f"{self.patient.name} -- {self.branch.brand_name}"

class DoctorWallet(models.Model):
    user = models.OneToOneField(Doctor, on_delete=models.CASCADE, related_name="doctorwallet") # db_index=True removed
    balance = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Doctor Wallets"
        ordering = ['user__name']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.balance}"
    
class PharmacyWallet(models.Model):
    user = models.OneToOneField(Pharmacy, on_delete=models.CASCADE, related_name="pharmacywallet") # db_index=True removed
    balance = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Pharmacy Wallets"
        ordering = ['user__name']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.name} - {self.balance}"
    
class DoctorPayment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="paytodoctor") # db_index=True removed
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="paytodoctorfrompatient") # db_index=True removed
    datetimestamp = models.DateTimeField(auto_now_add=True) # db_index=True removed
    amount = models.FloatField(default=0.0)
    cash_payment = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    tran_id = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Doctor Payments"
        ordering = ['-datetimestamp', 'doctor__name', 'patient__name']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['doctor']),
            models.Index(fields=['datetimestamp']),
            models.Index(fields=['tran_id']),
            models.Index(fields=['doctor', '-datetimestamp']), # Get payments for a doctor by date
            models.Index(fields=['patient', '-datetimestamp']), # Get payments by a patient by date
            models.Index(fields=['doctor', 'patient']), # Payments between a specific doctor and patient
            models.Index(fields=['cash_payment', '-datetimestamp']), # Filter by payment type and date
        ]

    def __str__(self):
        return f"{self.patient.name} paid {self.amount} BDT to {self.doctor.name}"

class PharmacyPayment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="paytopharmacy") # db_index=True removed
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="paytopharmacyfrompatient") # db_index=True removed
    datetimestamp = models.DateTimeField(auto_now_add=True) # db_index=True removed
    amount = models.FloatField(default=0.0)
    cash_payment = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    tran_id = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Pharmacy Payments"
        ordering = ['-datetimestamp', 'pharmacy__name', 'patient__name']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['pharmacy']),
            models.Index(fields=['datetimestamp']),
            models.Index(fields=['tran_id']),
            models.Index(fields=['pharmacy', '-datetimestamp']),
            models.Index(fields=['patient', '-datetimestamp']),
            models.Index(fields=['pharmacy', 'patient']),
            models.Index(fields=['cash_payment', '-datetimestamp']),
        ]

    def __str__(self):
        return f"{self.patient.name} paid {self.amount} BDT to {self.pharmacy.name}"
    
class HospitalWallet(models.Model):
    user = models.OneToOneField(Hospital, on_delete=models.CASCADE, related_name="hospitalwallet") # db_index=True removed
    balance = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Hospital Wallets"
        ordering = ['user__brand_name']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.brand_name} - {self.balance}"
    
class DiagnosticWallet(models.Model):
    user = models.OneToOneField(Diagnostic, on_delete=models.CASCADE, related_name="diagnosticwallet") # db_index=True removed
    balance = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Diagnostic Wallets"
        ordering = ['user__brand_name']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.brand_name} - {self.balance}"
    
class HospitalPharmacyWallet(models.Model):
    user = models.OneToOneField(HospitalPharmacy, on_delete=models.CASCADE, related_name="hospitalpharmacywallet") # db_index=True removed
    balance = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Hospital Pharmacy Wallets"
        ordering = ['user__brand_name']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.brand_name} - {self.balance}"
    
class HospitalPayment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="paytohospital") # db_index=True removed
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name="paytohospitalfrompatient") # db_index=True removed
    datetimestamp = models.DateTimeField(auto_now_add=True) # db_index=True removed
    amount = models.FloatField(default=0.0)
    cash_payment = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    tran_id = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Hospital Payments"
        ordering = ['-datetimestamp', 'hospital__brand_name', 'patient__name']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['hospital']),
            models.Index(fields=['datetimestamp']),
            models.Index(fields=['tran_id']),
            models.Index(fields=['hospital', '-datetimestamp']),
            models.Index(fields=['patient', '-datetimestamp']),
            models.Index(fields=['hospital', 'patient']),
            models.Index(fields=['cash_payment', '-datetimestamp']),
        ]

    def __str__(self):
        return f"{self.patient.name} paid {self.amount} BDT to {self.hospital.brand_name}"
    
class DiagnosticPayment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="paytodiagnostic") # db_index=True removed
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, related_name="paytodiagnosticfrompatient") # db_index=True removed
    datetimestamp = models.DateTimeField(auto_now_add=True) # db_index=True removed
    amount = models.FloatField(default=0.0)
    cash_payment = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    tran_id = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Diagnostic Payments"
        ordering = ['-datetimestamp', 'diagnostic__brand_name', 'patient__name']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['diagnostic']),
            models.Index(fields=['datetimestamp']),
            models.Index(fields=['tran_id']),
            models.Index(fields=['diagnostic', '-datetimestamp']),
            models.Index(fields=['patient', '-datetimestamp']),
            models.Index(fields=['diagnostic', 'patient']),
            models.Index(fields=['cash_payment', '-datetimestamp']),
        ]

    def __str__(self):
        return f"{self.patient.name} paid {self.amount} BDT to {self.diagnostic.brand_name}"
    
class HospitalPharmacyPayment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="paytohospitalpharmacy") # db_index=True removed
    hospital_pharmacy = models.ForeignKey(HospitalPharmacy, on_delete=models.CASCADE, related_name="paytohospitalpharmacyfrompatient") # db_index=True removed
    datetimestamp = models.DateTimeField(auto_now_add=True) # db_index=True removed
    amount = models.FloatField(default=0.0)
    cash_payment = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    tran_id = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Hospital Pharmacy Payments"
        ordering = ['-datetimestamp', 'hospital_pharmacy__brand_name', 'patient__name']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['hospital_pharmacy']),
            models.Index(fields=['datetimestamp']),
            models.Index(fields=['tran_id']),
            models.Index(fields=['hospital_pharmacy', '-datetimestamp']),
            models.Index(fields=['patient', '-datetimestamp']),
            models.Index(fields=['hospital_pharmacy', 'patient']),
            models.Index(fields=['cash_payment', '-datetimestamp']),
        ]

    def __str__(self):
        return f"{self.patient.name} paid {self.amount} BDT to {self.hospital_pharmacy.brand_name}"

class PharmacyStock(models.Model):
    pharmacy = models.OneToOneField(Pharmacy, on_delete=models.CASCADE, related_name="pharmacystock") # db_index=True removed
    drug_name = models.TextField(null=True, blank=True) # db_index=True removed
    supplier = models.TextField(null=True, blank=True) # db_index=True removed
    number_of_units = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Pharmacy Stocks"
        ordering = ['pharmacy__name', 'drug_name']
        indexes = [
            models.Index(fields=['pharmacy']),
            models.Index(fields=['drug_name']),
            models.Index(fields=['supplier']),
            models.Index(fields=['pharmacy', 'drug_name']), # Find stock for a pharmacy by drug name
            models.Index(fields=['drug_name', 'supplier']), # Find drugs by name and supplier
            models.Index(fields=['pharmacy', 'supplier']), # Find drugs from a supplier for a pharmacy
        ]

    def __str__(self):
        return f"Pharmacy ({self.pharmacy.name}) - {self.drug_name}"

class HospitalPharmacyStock(models.Model):
    pharmacy = models.OneToOneField(HospitalPharmacy, on_delete=models.CASCADE, related_name="hospitalpharmacystock") # db_index=True removed
    drug_name = models.TextField(null=True, blank=True) # db_index=True removed
    supplier = models.TextField(null=True, blank=True) # db_index=True removed
    number_of_units = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Hospital Pharmacy Stocks"
        ordering = ['pharmacy__brand_name', 'drug_name']
        indexes = [
            models.Index(fields=['pharmacy']),
            models.Index(fields=['drug_name']),
            models.Index(fields=['supplier']),
            models.Index(fields=['pharmacy', 'drug_name']),
            models.Index(fields=['drug_name', 'supplier']),
            models.Index(fields=['pharmacy', 'supplier']),
        ]

    def __str__(self):
        return f"Pharmacy ({self.pharmacy.brand_name}) - {self.drug_name}"

class Chamber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="chambers") # db_index=True removed
    address = models.TextField(null=True, blank=True)
    under_hospital = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters
    hospital_name = models.TextField(null=True, blank=True) # db_index=True removed
    fee = models.IntegerField(default=0)
    contact = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        verbose_name_plural = "Chambers"
        ordering = ['doctor__name', 'hospital_name']
        indexes = [
            models.Index(fields=['doctor']),
            models.Index(fields=['hospital_name']),
            models.Index(fields=['doctor', 'under_hospital']), # Find chambers for a doctor, filtered by hospital affiliation
            models.Index(fields=['hospital_name', 'doctor']), # Find chambers by hospital name and doctor
        ]

    def __str__(self):
        return f"{self.doctor.name} - {self.hospital_name}"

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments") # db_index=True removed
    chamber = models.ForeignKey(Chamber, on_delete=models.CASCADE, related_name="chamberappointments") # db_index=True removed
    booked_at = models.DateTimeField(auto_now_add=True) # db_index=True removed
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateField() # db_index=True removed
    appointment_time = models.TimeField() # db_index=True removed
    payment_status = models.BooleanField(default=False, db_index=True) # Keep db_index=True for boolean filters

    class Meta:
        verbose_name_plural = "Appointments"
        ordering = ['-appointment_date', '-appointment_time', 'patient__name', 'chamber__doctor__name']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['chamber']),
            models.Index(fields=['appointment_date']),
            models.Index(fields=['appointment_time']),
            models.Index(fields=['patient', '-appointment_date']), # Get a patient's appointments by date
            models.Index(fields=['chamber', 'appointment_date', 'appointment_time']), # Find appointments for a chamber on a specific date/time
            models.Index(fields=['payment_status', 'appointment_date']), # Filter appointments by payment status and date
            models.Index(fields=['appointment_date', 'appointment_time', 'chamber']), # For scheduling checks
            models.Index(fields=['patient', 'chamber']), # For specific patient-chamber appointment history
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.chamber.doctor.name} - {self.appointment_date}"