import pandas as pd

# Define column names
columns = ['Name', 'Age', 'City']

# Empty list to hold rows
data = []

# Ask user how many rows to enter
try:
    n = int(input("How many records do you want to enter? "))
except:
    print("Invalid input. Using default of 3 records.")
    n = 3

# Loop for user input
for i in range(n):
    print(f"\nEnter details for person {i+1}:")
    name = input("Name: ")
    age = input("Age: ")
    city = input("City: ")

    # Append row to data list
    data.append([name, age, city])

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save to CSV
file_name = 'input_data.csv'
df.to_csv(file_name, index=False)

print(f"\nCSV file '{file_name}' has been created successfully!")
print("\nHere is your data:")
print(df)