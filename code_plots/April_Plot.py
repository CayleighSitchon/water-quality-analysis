import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV data
df = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\April2025_Data.xlsx')

# Quick look at your data
print(df.head())
print(df.columns)
print(df.info())

#Cleaning the data
df.columns = df.columns.str.strip()
print(df.isnull().sum()) #Drop rowes with any nulls

# Filter out standard rows
df_samples = df[df['Type'] != 'STD']

# Remove Lims IDs that include decimal points (diluted conc not needed)
df_samples = df_samples[~df_samples['Lims ID'].str.contains(r'\d+\.\d+', regex=True)]

# Ensure Concentration is numeric (coerce errors into NaN)
df_samples['Concentration'] = pd.to_numeric(df_samples['Concentration'], errors='coerce')
print(df_samples)
# Drop rows where Concentration is NaN
df_samples = df_samples.dropna(subset=['Concentration'])


# Calculating average concentration for elements per location
avg_concentration = df_samples.groupby(['Lims ID', 'Element'])['Concentration'].mean().reset_index()
print(avg_concentration)

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(14, 8))
sns.barplot(data=avg_concentration, x='Lims ID', y='Concentration', hue='Element')
plt.title('April Average Element Concentration by Location')
plt.xlabel('Sample', fontsize=12, fontweight='bold')
plt.ylabel('Average Concentration (ppm)', fontsize=12, fontweight='bold')
plt.xticks(rotation=25)
sns.set(style='whitegrid')  # Options: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("april_avg_concentration.png", dpi=300)
plt.show()