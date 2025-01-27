
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import os

# Correct file path
file_path = (r"C:\Users\SIR GOOD\Downloads\RewardsData.csv")
try:
    # Load the file
    data = pd.read_csv(file_path)
    print("File loaded successfully!")
    print(data.head())  # Display first 5 rows
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Correct file path
file_path = r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\RewardsData.csv"

# Load the file
data = pd.read_csv(file_path)

# Remove the 'Tags' column
data = data.drop(columns=['Tags'])

# Display the updated DataFrame
print(data.head())

# (Optional) Save the updated DataFrame back to a new CSV file
output_file_path = r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\RewardsData_Without_Tags.csv"
data.to_csv(output_file_path, index=False)
print(f"Updated file saved to: {output_file_path}")

# Correct file path
file_path = r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\RewardsData_Without_Tags.csv"

# Load the file
data = pd.read_csv(file_path)

# Get all unique values from the 'City' column and sort them alphabetically
unique_cities = sorted(data['City'].dropna().unique())

# Display the sorted list of cities
print("Unique cities in alphabetical order:")
print(unique_cities)

# Optional: Save the unique cities to a file
output_file_path = r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\Unique_Cities.txt"
with open(output_file_path, "w") as file:
    for city in unique_cities:
        file.write(city + "\n")

print(f"Unique cities saved to: {output_file_path}")

# Load the dataset
file_path = r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\RewardsData.csv"
df = pd.read_csv(file_path)

# Standardize the 'City' column
df['City'] = df['City'].replace({
    'Winston Salem': 'Winston-Salem',
    'Winston salem': 'Winston-Salem',
    'winston salem': 'Winston-Salem',
    'Winston-Salem, NC': 'Winston-Salem',
    'Winston-Salem ': 'Winston-Salem',
    'Winston-Salem,': 'Winston-Salem'
})

# Save the cleaned file
output_path = r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\Cleaned_RewardsData.csv"
df.to_csv(output_path, index=False)

print("All variations of 'Winston-salem' have been standardized.")
print(f"Cleaned file saved to: {output_path}")

# Load the CSV file
df = pd.read_csv(r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\Cleaned_RewardsData.csv")

# Apply title case to the 'City' column
df['City'] = df['City'].str.title()

# Save the updated file
df.to_csv(r"C:\Users\SIR GOOD\Desktop\EXAMINATON ANSWERS\City_Corrected_RewardsData.csv", index=False)

print("City names corrected and saved to 'City_Corrected_RewardsData.csv'.")

#Replace all format of te winston-salem with winston-salem
df['City'] = df['City'].str.replace

# Proper case for city names
df['City'] = df['State'].str.title()

# Display the first few rows to ensure everything is correct
df['State'] = df['State'].str.title()

# Replace state abbreviations with full names
us_states_abbrev = { 
'Abbreviation': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI',
'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 
'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
'Name': ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 
'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 
'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 
'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 
'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 
'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 
'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
}


abbrev_to_state = {v: k for v, k in us_states_abbrev.items()}
df['State'] = df['State'].replace (us_states_abbrev)

# Step g: Fill NaN in 'State' with state names in alphabetical order
states = sorted(us_states_abbrev.keys())
nan_indices = df[df['State'].isna()].index
for i, idx in enumerate(nan_indices):
    df.at[idx, 'State'] = states[i % len(states)]

# # Step h: Truncate ZIP codes longer than 5 digits
df['Zip'] = df['Zip'].astype(str).str[:5]

# # Step i: Drop rows with ZIP codes less than 5 digits
df = df[df['Zip'].str.len() == 5]

# # Step j: Convert 'Birthdate' to datetime
df['Birthdate'] = pd.to_datetime(df['Birthdate'], errors='coerce').dt.date

# # Step k-m: Save the resulting DataFrame to a PostgreSQL database
postgres_user = 'postgres'
postgres_password = 'lucy'
postgres_host = 'localhost'
postgres_port = '5432'
postgres_db = 'RewardsData'
db_url = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'

engine = create_engine(db_url)

# create database if not exist
if not database_exists(db_url):
    create_database(db_url)

table_name = 'CleanRewardsData'
df.to_sql(table_name, 'con=engine', if_exists='replace', index=False)

# save dataframe to postgres if_exist replace
df.to_sql(table_name, con=engine, if_exist='replace', index=False)

print(f"Data processed and saved to PostgreSQL database '{postgres_db}' in table '{table_name}'!")
