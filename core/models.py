from django.db import models

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