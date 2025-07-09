from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

from django.utils import timezone
from datetime import timedelta
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .validators import validate_file_extension
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
        ADMIN = 'admin', _('Admin')
        PHARMACY = 'pharmacy', _('Pharmacy')
        HOSPITAL = 'hospital', _('Hospital')
        DUTY_DOCTOR = 'duty_doctor', _('Duty Doctor')
        HOSPITAL_EMPLOYEE = 'hospital_employee', _('Hospital Employee')
        HOSPITAL_PHARMACY = 'hospital_pharmacy', _('Hospital Pharmacy')

    username = models.CharField(
        max_length=150,
        unique=True
    )
    
    name = models.CharField(_('full name'), max_length=255, blank=True)
    
    role = models.CharField(
        _('role'),
        max_length=30,
        choices=Roles.choices,
        default=Roles.PATIENT
    )
    
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['role']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

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
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nid = models.CharField(max_length=255, null=True, blank=True)
    brn = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True)
    bg = models.CharField(max_length=255, null=True, blank=True)
    religion = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.phone} - {self.address}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nid = models.CharField(max_length=255, null=True, blank=True)
    brn = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True)
    bg = models.CharField(max_length=255, null=True, blank=True)
    religion = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    bmdc = models.CharField(max_length=255, unique=True, null=False, default='Duty Doctor')
    qualifications = models.TextField(null=True, blank=True)
    job_location = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.name} - {self.bmdc} - {self.address}"
    
class Pharmacy(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nid = models.CharField(max_length=255, null=True, blank=True)
    brn = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    sex = models.CharField(max_length=255, null=True, blank=True)
    bg = models.CharField(max_length=255, null=True, blank=True)
    religion = models.CharField(max_length=255, null=True, blank=True)
    marital_status = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    trade_lic = models.CharField(max_length=255, unique=True, null=False, default='Duty Doctor')
    pharmacy_image = models.ImageField(upload_to='pharmacy_images/',null=False)
    pharmacy_location = models.TextField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.phone} - {self.address}"
    
class FamilyMember(models.Model):
    username1 = models.OneToOneField(User, on_delete=models.CASCADE,related_name="main_member")
    username2 = models.OneToOneField(User, on_delete=models.CASCADE,related_name="related_member")
    relation = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.username1} is {self.relation} of {self.username2}"