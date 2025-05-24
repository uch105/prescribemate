from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('individual_doctor', 'Individual Doctor'),
        ('duty_doctor', 'Duty Doctor'),
        ('patient', 'Patient'),
        ('pharmacy', 'Pharmacy'),
        ('hospital', 'Hospital Management'),
    ]

    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Optional role-specific fields
    bmdc_id = models.CharField(max_length=50, blank=True, null=True)
    nid = models.CharField(max_length=20, blank=True, null=True)
    trade_license = models.CharField(max_length=100, blank=True, null=True)

    hospital = models.ForeignKey('hospitals.Hospital', null=True, blank=True, on_delete=models.SET_NULL)
    designation = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"