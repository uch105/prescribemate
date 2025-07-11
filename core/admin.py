from django.contrib import admin
from .models import *
from common.models import *

admin.site.register(User)
admin.site.register(Drug)
admin.site.register(DrugGeneric)
admin.site.register(Ambulance)
admin.site.register(BloodDonor)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Pharmacy)
admin.site.register(FamilyMember)
'''
admin.site.register(Hospital)
admin.site.register(HospitalAdmission)
admin.site.register(HospitalBranch)
admin.site.register(HospitalChamber)
admin.site.register(HospitalCoupon)
admin.site.register(HospitalEmployee)
admin.site.register(HospitalTest)
admin.site.register(HospitalWard)
admin.site.register(HospitalWardBed)
admin.site.register(HospitalTestResult)
admin.site.register(Chamber)
admin.site.register(ChamberAppointment)
'''