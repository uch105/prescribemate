from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Drug(models.Model):
    drugs_id = models.CharField(primary_key=True)
    brand = models.TextField(null=True, blank=True)
    generic = models.TextField(null=True, blank=True)
    manufacturer = models.TextField(null=True, blank=True)
    strength = models.TextField(null=True, blank=True)
    applicable_for = models.TextField(null=True, blank=True)
    indication = models.TextField(null=True, blank=True)
    contraindication = models.TextField(null=True, blank=True)
    side_effect = models.TextField(null=True, blank=True)
    dosage_administration = models.TextField(null=True, blank=True)
    theraputic_class = models.TextField(null=True, blank=True)
    price = models.TextField(default="Not specified")
    pregnancy_lactation = models.TextField(null=True, blank=True)
    interaction = models.TextField(null=True, blank=True)
    mode_of_action = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.brand
    
class DrugGeneric(models.Model):
    generic_name = models.TextField(unique=True,db_index=True)
    indications_list = models.TextField(null=True, blank=True)
    contraindications_list = models.TextField(null=True, blank=True)
    side_effects_list = models.TextField(null=True, blank=True)
    theraputic_classes_list = models.TextField(null=True, blank=True)
    dosage_administrations = models.TextField(null=True, blank=True)
    dosage_administrations_list = models.TextField(null=True, blank=True)
    pregnancy_lactations = models.TextField(null=True, blank=True)
    interactions = models.TextField(null=True, blank=True)
    mechanism_of_actions = models.TextField(null=True, blank=True)
    precautions_warnings = models.TextField(null=True, blank=True)
    storage = models.TextField(null=True, blank=True)
    overdose = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.generic_name

class Ambulance(models.Model):
    ambulance_id = models.CharField(max_length=255, primary_key=True)
    ambulance_name = models.CharField(max_length=255,null=True, blank=True)
    ambulance_owner_name = models.CharField(max_length=255, null=True, blank=True)
    contact_no = models.CharField(max_length=255,null=True, blank=True)
    verified = models.BooleanField(default=False)
    operating_area = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.ambulance_owner_name} -- {self.operating_area}"

class BloodDonor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    donated = models.IntegerField(default=0)
    last_donated = models.DateField()
    area = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.name} -- {self.area} -- {self.last_donated}"