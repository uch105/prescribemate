import pandas as pd
from decouple import config

corefiles_path = config('COREFILES_PATH')
drugs_xlsx_path = corefiles_path+'drugs.xlsx'
company_names_path = corefiles_path+'company_names.txt'

df = pd.read_excel(drugs_xlsx_path)

company_names = df.iloc[:, 0].dropna().drop_duplicates()

unique_company_names = sorted(list(company_names))

with open(company_names_path, 'w') as f:
    for name in unique_company_names:
        f.write(name + '\n')

print(f"Saved {len(unique_company_names)} unique company names to corefiles/company_names.txt")