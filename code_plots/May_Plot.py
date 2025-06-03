import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV data
df = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\Kern_Data.xlsx')

# Quick look at your data
print(df.head())
print(df.columns)
print(df.info())

#Cleaning the data
df.columns = df.columns.str.strip()
print(df.isnull().sum()) #Drop rowes with any nulls

#Filter out standard rows
# Filter out standard rows
df_samples = df

# Ensure Concentration is numeric (coerce errors into NaN)
df_samples['Concentration'] = pd.to_numeric(df_samples['Concentration'], errors='coerce')

# Drop rows where Concentration is NaN
df_samples = df_samples.dropna(subset=['Concentration'])


# Calculating average concentration for elements per location
avg_concentration = df_samples.groupby(['Lims ID', 'Element'])['Concentration'].mean().reset_index()
print(avg_concentration)

#Creating the bar plot
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(20, 8)) #Creates a blank area for the plot and sets the figure to size
sns.barplot(data=avg_concentration, x='Lims ID', y='Concentration', hue='Element') #creates the bar plot, hue means
plt.title('Average Element Concentration by Location')
plt.xlabel('Sample', fontsize=12, fontweight='bold')
plt.ylabel('Average Concentration (ppm)', fontsize=12, fontweight='bold')
plt.xticks(rotation=25)
sns.set(style='whitegrid')  # Options: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("may_avg_concentration.png", dpi=300)
plt.show()





