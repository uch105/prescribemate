from django.contrib import admin
from .models import *
from common.models import *

# Assuming your models are in apps named 'core' and 'common'
# You might need to adjust imports based on your actual app structure.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

# Unregister default User model if you're using a custom User model
# admin.site.unregister(User) # Uncomment if your custom User model is in common.models

# Custom User Admin
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'name', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'name', 'role')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    readonly_fields = ('date_joined','last_login')

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group) # Often unregistered when using custom User model

# Admin for core app models
@admin.register(HospitalRegistrationRequest)
class HospitalRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'reg_code', 'legal_contact')
    search_fields = ('brand_name', 'reg_code', 'legal_contact')
    list_filter = ('brand_name',)
    ordering = ('brand_name',)

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ('brand', 'generic', 'manufacturer', 'strength', 'theraputic_class', 'price')
    search_fields = ('brand', 'generic', 'manufacturer', 'theraputic_class', 'indication', 'contraindication')
    list_filter = ('manufacturer', 'theraputic_class')
    ordering = ('brand',)

@admin.register(DrugGeneric)
class DrugGenericAdmin(admin.ModelAdmin):
    list_display = ('generic_name', 'theraputic_classes_list')
    search_fields = ('generic_name', 'theraputic_classes_list', 'indications_list')
    ordering = ('generic_name',)

@admin.register(Ambulance)
class AmbulanceAdmin(admin.ModelAdmin):
    list_display = ('ambulance_name', 'ambulance_owner_name', 'contact_no', 'operating_area', 'verified')
    search_fields = ('ambulance_name', 'ambulance_owner_name', 'contact_no', 'operating_area')
    list_filter = ('verified', 'operating_area')
    ordering = ('ambulance_name',)

@admin.register(CC)
class CCAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)
    ordering = ('text',)

@admin.register(OE)
class OEAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)
    ordering = ('text',)

@admin.register(RF)
class RFAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)
    ordering = ('text',)

@admin.register(DX)
class DXAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)
    ordering = ('text',)

@admin.register(IX)
class IXAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)
    ordering = ('text',)


# Admin for common app models

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('username1', 'username2', 'relation')
    search_fields = ('username1__username', 'username2__username', 'relation')
    list_filter = ('relation',)
    raw_id_fields = ('username1', 'username2') # Use raw_id_fields for large user bases
    ordering = ('username1__username',)

@admin.register(BloodDonor)
class BloodDonorAdmin(admin.ModelAdmin):
    list_display = ('user', 'donated', 'last_donated', 'area')
    search_fields = ('user__name', 'user__username', 'area')
    list_filter = ('last_donated', 'area')
    raw_id_fields = ('user',)
    ordering = ('user__name',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'sex', 'bg', 'nid', 'brn')
    search_fields = ('name', 'phone', 'nid', 'brn', 'address')
    list_filter = ('sex', 'bg', 'religion', 'marital_status')
    raw_id_fields = ('user',)
    ordering = ('name',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bmdc', 'phone', 'sex', 'job_location', 'verified')
    search_fields = ('name', 'bmdc', 'phone', 'job_location', 'qualifications')
    list_filter = ('sex', 'verified', 'job_location')
    raw_id_fields = ('user',)
    ordering = ('name',)

@admin.register(Pharmacy)
class PharmacyAdmin(admin.ModelAdmin):
    list_display = ('name', 'trade_lic', 'phone', 'pharmacy_location', 'verified')
    search_fields = ('name', 'trade_lic', 'phone', 'pharmacy_location')
    list_filter = ('verified', 'pharmacy_location')
    raw_id_fields = ('user',)
    ordering = ('name',)

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'reg_code', 'district', 'upazilla', 'verified')
    search_fields = ('brand_name', 'reg_code', 'district', 'upazilla', 'address', 'legal_contact')
    list_filter = ('verified', 'facility_type', 'category', 'district', 'upazilla')
    ordering = ('brand_name',)
    #readonly_fields = ('expiration_date', 'days_remaining') # Display these properties but don't allow editing

@admin.register(HospitalPharmacy)
class HospitalPharmacyAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'reg_code', 'district', 'upazilla', 'verified')
    search_fields = ('brand_name', 'reg_code', 'district', 'upazilla', 'address', 'legal_contact')
    list_filter = ('verified', 'facility_type', 'category', 'district', 'upazilla')
    ordering = ('brand_name',)

@admin.register(HospitalEmployee)
class HospitalEmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital', 'role', 'security_id')
    search_fields = ('user__name', 'user__username', 'hospital__brand_name', 'role', 'security_id')
    list_filter = ('role', 'hospital')
    raw_id_fields = ('user', 'hospital')
    ordering = ('user__name',)

@admin.register(HospitalWard)
class HospitalWardAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'ward')
    search_fields = ('hospital__brand_name', 'ward')
    list_filter = ('hospital',)
    raw_id_fields = ('hospital',)
    ordering = ('hospital__brand_name', 'ward')

@admin.register(HospitalWardBed)
class HospitalWardBedAdmin(admin.ModelAdmin):
    list_display = ('ward', 'bed_type', 'bed_price', 'is_available', 'current_patient')
    search_fields = ('ward__hospital__brand_name', 'ward__ward', 'bed_type', 'current_patient__name')
    list_filter = ('is_available', 'bed_type', 'ward__hospital')
    raw_id_fields = ('ward', 'current_patient')
    ordering = ('ward__hospital__brand_name', 'ward__ward', 'bed_type')

@admin.register(Diagnostic)
class DiagnosticAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'reg_code', 'district', 'upazilla', 'verified')
    search_fields = ('brand_name', 'reg_code', 'district', 'upazilla', 'address', 'legal_contact')
    list_filter = ('verified', 'facility_type', 'category', 'district', 'upazilla')
    ordering = ('brand_name',)

@admin.register(DiagnosticEmployee)
class DiagnosticEmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'hospital', 'role', 'security_id')
    search_fields = ('user__name', 'user__username', 'hospital__brand_name', 'role', 'security_id')
    list_filter = ('role', 'hospital')
    raw_id_fields = ('user', 'hospital')
    ordering = ('user__name',)

@admin.register(DiagnosticTest)
class DiagnosticTestAdmin(admin.ModelAdmin):
    list_display = ('testID', 'test_name', 'hospital_branch', 'price', 'daily_limit', 'current_usage', 'last_reset_date')
    search_fields = ('testID', 'test_name', 'hospital_branch__brand_name')
    list_filter = ('hospital_branch', 'last_reset_date')
    raw_id_fields = ('hospital_branch',)
    ordering = ('test_name',)

@admin.register(DiagnosticTestResult)
class DiagnosticTestResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'creation_date', 'updated_date')
    search_fields = ('user__username', 'test__test_name', 'result')
    list_filter = ('creation_date', 'test__hospital_branch')
    raw_id_fields = ('user', 'test')
    ordering = ('-creation_date',)

@admin.register(HospitalCoupon)
class HospitalCouponAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'coupon_name', 'off_amount')
    search_fields = ('hospital__brand_name', 'coupon_name')
    list_filter = ('hospital',)
    raw_id_fields = ('hospital',)
    ordering = ('hospital__brand_name', 'coupon_name')

@admin.register(DiagnosticCoupon)
class DiagnosticCouponAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'coupon_name', 'off_amount')
    search_fields = ('hospital__brand_name', 'coupon_name')
    list_filter = ('hospital',)
    raw_id_fields = ('hospital',)
    ordering = ('hospital__brand_name', 'coupon_name')

@admin.register(HospitalAdmission)
class HospitalAdmissionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'branch', 'admission_time', 'leave_time')
    search_fields = ('patient__name', 'branch__brand_name', 'admissioninfo')
    list_filter = ('admission_time', 'branch')
    raw_id_fields = ('patient', 'branch')
    ordering = ('-admission_time',)

@admin.register(DoctorWallet)
class DoctorWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__name', 'user__bmdc')
    raw_id_fields = ('user',)
    ordering = ('user__name',)

@admin.register(PharmacyWallet)
class PharmacyWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__name', 'user__trade_lic')
    raw_id_fields = ('user',)
    ordering = ('user__name',)

@admin.register(DoctorPayment)
class DoctorPaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'amount', 'datetimestamp', 'cash_payment', 'tran_id')
    search_fields = ('patient__name', 'doctor__name', 'tran_id', 'description')
    list_filter = ('cash_payment', 'datetimestamp', 'doctor')
    raw_id_fields = ('patient', 'doctor')
    ordering = ('-datetimestamp',)

@admin.register(PharmacyPayment)
class PharmacyPaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'pharmacy', 'amount', 'datetimestamp', 'cash_payment', 'tran_id')
    search_fields = ('patient__name', 'pharmacy__name', 'tran_id', 'description')
    list_filter = ('cash_payment', 'datetimestamp', 'pharmacy')
    raw_id_fields = ('patient', 'pharmacy')
    ordering = ('-datetimestamp',)

@admin.register(HospitalWallet)
class HospitalWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__brand_name',)
    raw_id_fields = ('user',)
    ordering = ('user__brand_name',)

@admin.register(DiagnosticWallet)
class DiagnosticWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__brand_name',)
    raw_id_fields = ('user',)
    ordering = ('user__brand_name',)

@admin.register(HospitalPharmacyWallet)
class HospitalPharmacyWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__brand_name',)
    raw_id_fields = ('user',)
    ordering = ('user__brand_name',)

@admin.register(HospitalPayment)
class HospitalPaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'hospital', 'amount', 'datetimestamp', 'cash_payment', 'tran_id')
    search_fields = ('patient__name', 'hospital__brand_name', 'tran_id', 'description')
    list_filter = ('cash_payment', 'datetimestamp', 'hospital')
    raw_id_fields = ('patient', 'hospital')
    ordering = ('-datetimestamp',)

@admin.register(DiagnosticPayment)
class DiagnosticPaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'diagnostic', 'amount', 'datetimestamp', 'cash_payment', 'tran_id')
    search_fields = ('patient__name', 'diagnostic__brand_name', 'tran_id', 'description')
    list_filter = ('cash_payment', 'datetimestamp', 'diagnostic')
    raw_id_fields = ('patient', 'diagnostic')
    ordering = ('-datetimestamp',)

@admin.register(HospitalPharmacyPayment)
class HospitalPharmacyPaymentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'hospital_pharmacy', 'amount', 'datetimestamp', 'cash_payment', 'tran_id')
    search_fields = ('patient__name', 'hospital_pharmacy__brand_name', 'tran_id', 'description')
    list_filter = ('cash_payment', 'datetimestamp', 'hospital_pharmacy')
    raw_id_fields = ('patient', 'hospital_pharmacy')
    ordering = ('-datetimestamp',)

@admin.register(PharmacyStock)
class PharmacyStockAdmin(admin.ModelAdmin):
    list_display = ('pharmacy', 'drug_name', 'supplier', 'number_of_units', 'price')
    search_fields = ('pharmacy__name', 'drug_name', 'supplier')
    list_filter = ('pharmacy',)
    raw_id_fields = ('pharmacy',)
    ordering = ('pharmacy__name', 'drug_name')

@admin.register(HospitalPharmacyStock)
class HospitalPharmacyStockAdmin(admin.ModelAdmin):
    list_display = ('pharmacy', 'drug_name', 'supplier', 'number_of_units', 'price')
    search_fields = ('pharmacy__brand_name', 'drug_name', 'supplier')
    list_filter = ('pharmacy',)
    raw_id_fields = ('pharmacy',)
    ordering = ('pharmacy__brand_name', 'drug_name')

@admin.register(Chamber)
class ChamberAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'hospital_name', 'fee', 'under_hospital')
    search_fields = ('doctor__name', 'hospital_name', 'address')
    list_filter = ('under_hospital', 'doctor')
    raw_id_fields = ('doctor',)
    ordering = ('doctor__name', 'hospital_name')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'chamber', 'appointment_date', 'appointment_time', 'payment_status', 'booked_at')
    search_fields = ('patient__name', 'chamber__doctor__name', 'chamber__hospital_name')
    list_filter = ('payment_status', 'appointment_date', 'chamber__doctor', 'chamber__hospital_name')
    raw_id_fields = ('patient', 'chamber')
    ordering = ('-appointment_date', '-appointment_time')
