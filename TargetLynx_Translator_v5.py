import pandas as pd
import re

# File paths
input_file = 'C:\\Users\\georg\\OneDrive\\Documents\\Real Life!\\Michigan\\Balbach_Lab_PostDoc\\Human_experiments\\EX_n_documentation\\EX_4_20250212_KW2\\20250224_KW_2_rerun_integrated.txt'
output_file = 'C:\\Users\\georg\\OneDrive\\Documents\\Real Life!\\Michigan\\Balbach_Lab_PostDoc\\Human_experiments\\EX_n_documentation\\EX_4_20250212_KW2\\KW2_rerun_python_output_2.xlsx'

# Data storage
data = []
current_compound = None
current_isotopologue = None

# Read the text file
with open(input_file, 'r') as file:
    for line in file:
        line = line.strip()

        # Capture compound name
        compound_match = re.match(r'Compound \d+:\s+(.*)', line)
        if compound_match:
            current_compound = compound_match.group(1)
            continue

        # Skip header and empty lines
        if line.startswith('#') or not line:
            continue

        # Split and capture row data
        fields = re.split(r'\t+', line)
        if len(fields) >= 8:
            # Exclude blanks and media control samples
            if 'blank' in fields[2].lower() or 'mediacontrol' in fields[2].lower():
                continue

            # Extract isotopologue (like m+0, m+1, etc.) from compound name
            isotopologue_match = re.search(r'm\+\d+', current_compound)
            isotopologue = isotopologue_match.group(0) if isotopologue_match else 'm+0'

            # Extract base compound name without isotopologue and remove special characters
            base_compound = re.sub(r'\s+m\+\d+', '', current_compound)
            base_compound = re.sub(r'[*/\\?:\[\]]', '', base_compound)  # Remove special characters

            entry = {
                'Compound': base_compound,
                'Sample_ID': fields[1],
                'Name': fields[2],
                'Isotopologue': isotopologue,
                'Area': float(fields[5]) if fields[5] else 0.0
            }
            data.append(entry)

# Convert to DataFrame
df = pd.DataFrame(data)

# Pivot table to get one sheet per compound and one column per isotopologue
with pd.ExcelWriter(output_file) as writer:
    for compound in df['Compound'].unique():
        compound_df = df[df['Compound'] == compound]
        pivot_df = compound_df.pivot_table(index='Name', columns='Isotopologue', values='Area', fill_value=0)
        
        # Ensure 'm+0' exists to prevent KeyError
        if 'm+0' not in pivot_df.columns:
            pivot_df['m+0'] = 0
        
        pivot_df['Total_Abundance'] = pivot_df.sum(axis=1)
        
        # Avoid division by zero errors
        pivot_df['m+0_%'] = (pivot_df['m+0'] / pivot_df['Total_Abundance'].replace(0, 1) * 100).round(2)
        pivot_df['m+1_to_m+n_%'] = ((pivot_df['Total_Abundance'] - pivot_df['m+0']) / pivot_df['Total_Abundance'].replace(0, 1) * 100).round(2)
        
        pivot_df.to_excel(writer, sheet_name=compound)

print(f"Data successfully written to {output_file}")
