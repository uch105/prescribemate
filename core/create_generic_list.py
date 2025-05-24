import pandas as pd

# Read the Excel file
df = pd.read_excel('drugs.xlsx')

# Extract column C (Generic Names), drop duplicates, and drop NA values
generic_names = df.iloc[:, 2].dropna().drop_duplicates()

# Convert to list and sort alphabetically
unique_generic_names = sorted(list(generic_names))

# Save to text file
with open('/home/uch/prescribemate/core/corefiles/generic_names.txt', 'w') as f:
    for name in unique_generic_names:
        f.write(name + '\n')

print(f"Saved {len(unique_generic_names)} unique generic names to corefiles/generic_names.txt")