import pandas as pd

# Input CSV file name
csv_file = 'input_data.csv'

# Output Excel file name
excel_file = 'input_data.xlsx'

# Read the CSV file
df = pd.read_csv(csv_file)

# Convert to Excel
df.to_excel(excel_file, index=False)

print(f"CSV file '{csv_file}' has been converted to Excel file '{excel_file}' successfully!")
