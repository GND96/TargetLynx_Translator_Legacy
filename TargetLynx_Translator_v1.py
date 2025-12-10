import pandas as pd
import re

# File paths
input_file = 'C:\\Users\\georg\\OneDrive\\Documents\\Real Life!\\Michigan\\Balbach_Lab_PostDoc\\Human_experiments\\EX_n_documentation\\EX_3_20250205\\clipfile_20250206_GD_1_GLuandFru.txt'
output_file = 'C:\\Users\\georg\\OneDrive\\Documents\\Real Life!\\Michigan\\Balbach_Lab_PostDoc\\Human_experiments\\EX_n_documentation\\EX_3_20250205\\formatted_results_pythonoutput1.xlsx'

# Data storage
data = []
current_compound = None

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
        if len(fields) >= 8:  # Ensure valid data row
            entry = {
                'Compound': current_compound,
                'Sample_ID': fields[1],
                'Name': fields[2],
                'RT': fields[4],
                'Area': fields[5],
                'Response': fields[7],
                'Flags': fields[8] if len(fields) > 8 else ''
            }
            data.append(entry)

# Convert to DataFrame
df = pd.DataFrame(data)

# Export to Excel
df.to_excel(output_file, index=False)
print(f"Data successfully written to {output_file}")