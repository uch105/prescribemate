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
    
class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255,null=True, blank=True)
    verified = models.BooleanField(default=False)
    joining_date = models.DateTimeField(auto_now_add=True)
    legal_contact = models.CharField(max_length=255, null=True)
    logo = models.ImageField(upload_to='hospital_images/')
    subscription_date = models.DateField()
    subscription_period = models.PositiveIntegerField(default=365)
    current_renewal_period = models.PositiveIntegerField(null=True, blank=True)
    
    @property
    def expiration_date(self):
        """Calculate expiration using either current_renewal_period or subscription_period"""
        period = self.current_renewal_period or self.subscription_period
        return self.subscription_date + timedelta(days=period)
    
    @property
    def is_subscription_valid(self):
        """Check if subscription is currently active"""
        return timezone.now().date() <= self.expiration_date
    
    @property
    def days_remaining(self):
        """Calculate days remaining until expiration"""
        remaining = (self.expiration_date - timezone.now().date()).days
        return max(0, remaining)
    
    def renew_subscription(self, period_days=None):
        """
        Renew subscription, optionally with custom period
        Args:
            period_days: None=use default, int=use custom period
        """

        if self.is_subscription_valid:
            self.subscription_date = self.expiration_date
        else:
            self.subscription_date = timezone.now().date()

        if period_days:
            self.current_renewal_period = period_days
        else:
            self.current_renewal_period = None
        
        self.save()
        return self
    '''
    def check_subscription_status(self):
        """
        Check subscription status and send notifications if needed
        Returns True if notification was sent
        """
        if self.days_remaining == 7:
            self._send_renewal_reminder()
            return True
        elif not self.is_subscription_valid:
            self._send_expiration_notification()
            return True
        return False
    
    def _send_renewal_reminder(self):
        """Send 7-day renewal reminder email"""
        subject = f"Renew your {self.brand_name} subscription (7 days remaining)"
        context = {
            'hospital': self,
            'expiration_date': self.expiration_date,
            'renew_url': f"{settings.SITE_URL}/renew-subscription"
        }
        
        text_message = render_to_string('emails/subscription_reminder.txt', context)
        html_message = render_to_string('emails/subscription_reminder.html', context)
        
        send_mail(
            subject,
            text_message,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email, self.legal_contact],
            html_message=html_message
        )

    def _send_expiration_notification(self):
        """Send subscription expired notification"""
        subject = f"Your {self.brand_name} subscription has expired"
        message = render_to_string('emails/subscription_expired.html', {
            'hospital': self,
            'renew_url': f"{settings.SITE_URL}/renew-subscription"
        })
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.user.email, self.legal_contact]
        )
    '''
    
    def __str__(self):
        status = "Active" if self.is_subscription_valid else "Expired"
        return f"{self.brand_name} - Subscription {status} ({self.days_remaining} days remaining)"

class HospitalBranch(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='branches')
    branch_name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True, blank=True)
    contact_no = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.hospital.brand_name} - {self.branch_name}"

class HospitalEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='branchemployees')
    role = models.CharField(max_length=255, default='Regular')
    security_id = models.CharField(max_length=255,null=True, blank=True)
    cv_file = models.FileField(
        upload_to=user_media_path,
        #validators=validate_file_extension,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.name} -- {self.role} -- {self.branch.branch_name}"

class HospitalWard(models.Model):
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='wards')
    ward = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.branch.branch_name} -- {self.ward}"
    
class HospitalWardBed(models.Model):
    ward = models.ForeignKey(HospitalWard, on_delete=models.CASCADE, related_name='wardbeds')
    bed_type = models.CharField(max_length=255, null=True, blank=True)
    bed_price = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    current_patient = models.ForeignKey(
        Patient,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='occupied_beds'
    )

    def __str__(self):
        return f"{self.ward.branch.branch_name} -- {self.ward.ward} -- {self.bed_type}"

class HospitalTest(models.Model):
    testID = models.CharField(max_length=255, primary_key=True)
    hospital_branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='tests')
    test_name  =  models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)
    daily_limit = models.IntegerField(default=0)
    current_usage = models.IntegerField(default=0)
    last_reset_date = models.DateField(auto_now_add=True)
    
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

class HospitalTestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usertests')
    test = models.ForeignKey(HospitalTest, on_delete=models.CASCADE, related_name='hospitaltests')
    creation_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    result = models.TextField(null=True,blank=True)
    file = models.FileField(upload_to=user_test_result_path,validators=[validate_file_extension], null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s {self.test.test_name} result"
    
class HospitalCoupon(models.Model):
    hospital = models.ForeignKey(Hospital,on_delete=models.CASCADE, related_name='coupons')
    coupon_name = models.CharField(max_length=255, null=True,blank=True)
    off_amount = models.CharField(max_length=100)

    def __str__(self):
        return f"({self.hospital.brand_name}) -- {self.coupon_name} -- {self.off_amount}"

class Chamber(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='chambers')
    location = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    limit = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.doctor.name} -- {self.location}"

class HospitalChamber(models.Model):
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='hospitalchambers')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctorhospitalchambers')
    limit = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.doctor.name} -- {self.branch.address}"
    
class HospitalAdmission(models.Model):
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name='hospitalpatients')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admitted_hospitals')
    admissioninfo =  models.TextField(null=True, blank=True)
    admission_time = models.DateTimeField(auto_now_add=True)
    leave_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.name} -- {self.branch.branch_name}"

class ChamberAppointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='chamber_appointments')
    chamber = models.ForeignKey(Chamber, on_delete=models.CASCADE, related_name='appointments')
    doctor_name = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(
        max_length=50,
        choices=[("pending", "Pending"), ("completed", "Completed"), ("cancelled", "Cancelled")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor_name} - {self.date} {self.time}"