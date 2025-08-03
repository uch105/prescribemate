import os
import sys
import django
from decouple import config

project_root = config("PROJECT_ROOT")
sys.path.append(project_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prescribemate.settings')
django.setup()

from common.models import Hospital, Diagnostic, HospitalWallet, DiagnosticWallet
import ast

d=0
h=0

with open("/home/uch/prescribemate/core/corefiles/hospital_names.txt", 'r', encoding='utf-8') as file:
    for line in file:
        data = ast.literal_eval(line.strip())
        if 'diagnostic' in data[2].lower():
            try:
                instance = Diagnostic.objects.filter(brand_name=data[0],reg_code=data[1],facility_type=data[2],category=data[3],district=data[4],upazilla=data[5],address=data[6])
                if instance.exists():
                    continue
                else:
                    instance = Diagnostic.objects.create(brand_name=data[0],reg_code=data[1],facility_type=data[2],category=data[3],district=data[4],upazilla=data[5],address=data[6])
                    DiagnosticWallet.objects.create(
                        user=instance,
                        balance=0.0,
                    )
                    d+=1
            except Exception as e:
                print(f"Error creating diagnostic: {e}")
                pass
        else:
            try:
                instance = Hospital.objects.filter(brand_name=data[0],reg_code=data[1],facility_type=data[2],category=data[3],district=data[4],upazilla=data[5],address=data[6])
                if instance.exists():
                    continue
                else:
                    instance = Hospital.objects.create(brand_name=data[0],reg_code=data[1],facility_type=data[2],category=data[3],district=data[4],upazilla=data[5],address=data[6])
                    HospitalWallet.objects.create(
                        user=instance,
                        balance=0.0,
                    )
                    h+=1
            except Exception as e:
                print(f"Error creating hospital: {e}")
                pass

print(f"Total Hospitals Created: {h}")
print(f"Total Diagnostics Created: {d}")
print("Database creation completed successfully.")