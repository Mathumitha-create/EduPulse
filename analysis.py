import pandas as pd

# Load dataset
df = pd.read_csv("data/dataset.csv")

print("\nFirst 5 Rows:")
print(df.head())

print("\nColumns:")
print(df.columns)

print("\nDataset Info:")
print(df.info())

print("\nSummary Statistics:")
print(df.describe())