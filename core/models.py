#---------- core/models.py --------------------

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class HospitalRegistrationRequest(models.Model):
    brand_name = models.TextField(null=True, blank=True) # db_index=True removed, covered by indexes
    reg_code = models.CharField(max_length=100, null=True, blank=True) # db_index=True removed
    legal_contact = models.CharField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    upazilla = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to="hospital_images/")

    class Meta:
        verbose_name_plural = "Hospital Registration Requests"
        ordering = ['brand_name']
        indexes = [
            models.Index(fields=['brand_name']), # For queries filtering only by brand_name
            models.Index(fields=['reg_code']), # For queries filtering only by reg_code
            models.Index(fields=['brand_name', 'reg_code']), # For queries filtering by both
        ]

    def __str__(self):
        return f"{self.brand_name} - {self.reg_code}"

class Drug(models.Model):
    drugs_id = models.CharField(primary_key=True)
    brand = models.TextField(null=True, blank=True) # db_index=True removed
    generic = models.TextField(null=True, blank=True) # db_index=True removed
    manufacturer = models.TextField(null=True, blank=True) # db_index=True removed
    strength = models.TextField(null=True, blank=True)
    applicable_for = models.TextField(null=True, blank=True)
    indication = models.TextField(null=True, blank=True)
    contraindication = models.TextField(null=True, blank=True)
    side_effect = models.TextField(null=True, blank=True)
    dosage_administration = models.TextField(null=True, blank=True)
    theraputic_class = models.TextField(null=True, blank=True) # db_index=True removed
    price = models.TextField(default="Not specified")
    pregnancy_lactation = models.TextField(null=True, blank=True)
    interaction = models.TextField(null=True, blank=True)
    mode_of_action = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Drugs"
        ordering = ['brand']
        indexes = [
            models.Index(fields=['brand']), # For queries filtering only by brand
            models.Index(fields=['generic']), # For queries filtering only by generic
            models.Index(fields=['manufacturer']), # For queries filtering only by manufacturer
            models.Index(fields=['theraputic_class']), # For queries filtering only by therapeutic class
            models.Index(fields=['brand', 'generic']), # For queries filtering by brand and generic
            models.Index(fields=['theraputic_class', 'brand']), # For queries filtering by class then brand
            models.Index(fields=['manufacturer', 'theraputic_class']), # For queries filtering by manufacturer and class
        ]

    def __str__(self):
        return self.brand
    
class DrugGeneric(models.Model):
    generic_name = models.TextField(unique=True, db_index=True) # Already indexed due to unique=True
    indications_list = models.TextField(null=True, blank=True)
    contraindications_list = models.TextField(null=True, blank=True)
    side_effects_list = models.TextField(null=True, blank=True)
    theraputic_classes_list = models.TextField(null=True, blank=True) # db_index=True removed
    dosage_administrations = models.TextField(null=True, blank=True)
    dosage_administrations_list = models.TextField(null=True, blank=True)
    pregnancy_lactations = models.TextField(null=True, blank=True)
    interactions = models.TextField(null=True, blank=True)
    mechanism_of_actions = models.TextField(null=True, blank=True)
    precautions_warnings = models.TextField(null=True, blank=True)
    storage = models.TextField(null=True, blank=True)
    overdose = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Drug Generics"
        ordering = ['generic_name']
        indexes = [
            models.Index(fields=['theraputic_classes_list']), # For queries filtering only by therapeutic class list
            models.Index(fields=['generic_name', 'theraputic_classes_list']), # For queries filtering by generic name and class list
        ]

    def __str__(self):
        return self.generic_name

class Ambulance(models.Model):
    ambulance_id = models.CharField(max_length=255, primary_key=True)
    ambulance_name = models.CharField(max_length=255,null=True, blank=True) # db_index=True removed
    ambulance_owner_name = models.CharField(max_length=255, null=True, blank=True) # db_index=True removed
    contact_no = models.CharField(max_length=255,null=True, blank=True)
    verified = models.BooleanField(default=False) # db_index=True removed
    operating_area = models.TextField(null=True, blank=True) # db_index=True removed

    class Meta:
        verbose_name_plural = "Ambulances"
        ordering = ['ambulance_name']
        indexes = [
            models.Index(fields=['ambulance_name']),
            models.Index(fields=['ambulance_owner_name']),
            models.Index(fields=['operating_area']),
            models.Index(fields=['verified']),
            models.Index(fields=['operating_area', 'verified']), # Search by area and verification status
            models.Index(fields=['ambulance_name', 'operating_area']), # Search by name and area
        ]

    def __str__(self):
        return f"{self.ambulance_owner_name} -- {self.operating_area}"

class CC(models.Model):
    text = models.TextField(null=True, blank=True, db_index=True) # Keep db_index=True for single field

    class Meta:
        verbose_name_plural = "CCs"
        ordering = ['text']
        # No additional indexes needed for single field

    def __str__(self):
        return self.text

class OE(models.Model):
    text = models.TextField(null=True, blank=True, db_index=True) # Keep db_index=True for single field

    class Meta:
        verbose_name_plural = "OEs"
        ordering = ['text']
        # No additional indexes needed for single field

    def __str__(self):
        return self.text
    
class RF(models.Model):
    text = models.TextField(null=True, blank=True, db_index=True) # Keep db_index=True for single field

    class Meta:
        verbose_name_plural = "RFs"
        ordering = ['text']
        # No additional indexes needed for single field

    def __str__(self):
        return self.text
    
class DX(models.Model):
    text = models.TextField(null=True, blank=True, db_index=True) # Keep db_index=True for single field

    class Meta:
        verbose_name_plural = "DXs"
        ordering = ['text']
        # No additional indexes needed for single field

    def __str__(self):
        return self.text
    
class IX(models.Model):
    text = models.TextField(null=True, blank=True, db_index=True) # Keep db_index=True for single field

    class Meta:
        verbose_name_plural = "IXs"
        ordering = ['text']
        # No additional indexes needed for single field

    def __str__(self):
        return self.text