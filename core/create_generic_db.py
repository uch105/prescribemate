import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prescribemate.settings')
django.setup()

from core.models import DrugGeneric
import json

with open('/home/uch/prescribemate/core/corefiles/merged_drugs.json', 'r') as f:
    data = json.load(f)

for drug in data["drugs"]:
    drug_generic = DrugGeneric(
        generic_name=drug["name"],
        indications_list="\n".join(drug.get("indications", [])),
        contraindications_list="\n".join(drug.get("contraindications", [])),
        side_effects_list="\n".join(drug.get("side_effects", [])),
        theraputic_classes_list="\n".join(drug.get("therapeutic_class", [])),
        dosage_administrations="\n".join(drug.get("dosage_&_administration", [])),
        dosage_administrations_list=None,
        pregnancy_lactations="\n".join(drug.get("pregnancy_&_lactation", [])),
        interactions="\n".join(drug.get("interaction", [])),
        mechanism_of_actions=None,
        precautions_warnings="\n".join(drug.get("precautions_&_warnings", [])),
        storage="\n".join(drug.get("storage_conditions", [])),
        overdose="\n".join(drug.get("overdose_effects", [])),
    )

    try:
        drug_generic.save()
        print(f'Successfully added {drug["name"]}')
    except Exception as e:
        print(f'Error adding {drug["name"]}: {e}')