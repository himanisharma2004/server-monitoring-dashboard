import pandas as pd

# Step 1: Load the dataset
file_path = "data/raw/Sample_Data_Ingestion.csv"
df = pd.read_csv(file_path)

# Step 2: Show first rows
print("First 5 rows of the dataset:")
print(df.head())

# Step 3: Dataset information
print("\nDataset Info:")
print(df.info())

# Step 4: Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Step 5: Remove duplicates
df = df.drop_duplicates()

# Step 6: Save cleaned dataset
output_path = "data/processed/clean_server_data.csv"
df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully.")