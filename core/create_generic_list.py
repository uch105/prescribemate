import pandas as pd
from decouple import config

corefiles_path = config('COREFILES_PATH')
drugs_xlsx_path = corefiles_path+'drugs.xlsx'
generic_names_path = corefiles_path+'generic_names.txt'

df = pd.read_excel(drugs_xlsx_path)

generic_names = df.iloc[:, 2].dropna().drop_duplicates()

unique_generic_names = sorted(list(generic_names))

with open(generic_names_path, 'w') as f:
    for name in unique_generic_names:
        f.write(name + '\n')

print(f"Saved {len(unique_generic_names)} unique generic names to corefiles/generic_names.txt")