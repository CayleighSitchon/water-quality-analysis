import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load monthly data
may = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\Kern_Data.xlsx')
apr = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\April2025_Data.xlsx')
mar = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\March2025_Data.xlsx')
jan = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\Jan2025_Data.xlsx')
feb = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\Feb2025_Data.xlsx')
oct = pd.read_excel(r'C:\Users\Cayle\OneDrive\water_quality_analyzer\data\Oct2024_Data.xlsx')

# Clean column names
for df in [may, apr, mar, jan, feb, oct]:
    df.columns = df.columns.str.strip()

# Add month labels
may['Month'] = 'May'
apr['Month'] = 'April'
mar['Month'] = 'March'
jan['Month'] = 'January'
feb['Month'] = 'February'
oct['Month'] = 'October'

# Combine data
all_data = pd.concat([may, apr, mar, jan, feb, oct], ignore_index=True)

# Convert 'Concentration' to numeric and drop NaNs
all_data['Concentration'] = pd.to_numeric(all_data['Concentration'], errors='coerce')
all_data = all_data.dropna(subset=['Concentration'])

# Remove diluted samples (e.g., Lims ID like 'Tollhouse1.1')
all_data['Lims ID'] = all_data['Lims ID'].astype(str)
all_data = all_data[~all_data['Lims ID'].str.contains(r'\d+\.\d+', regex=True)]

# Filter out DI and HNO samples (non-field samples)
all_data = all_data[~all_data['Lims ID'].str.contains('DI|HNO', case=False, na=False)]

# Extract base location name
all_data['Location'] = all_data['Lims ID'].str.extract(r'([A-Za-z\s]+)', expand=False).str.strip()


# Group by element and location to get mean concentrations
element_avg = all_data.groupby(['Element Label', 'Location'])['Concentration'].mean().reset_index()

#  If you want to limit to top 10 elements by overall concentration
top_elements = (all_data.groupby('Element Label')['Concentration']
                .mean().sort_values(ascending=False).head(10).index)
element_avg = element_avg[element_avg['Element Label'].isin(top_elements)]

# Pivot for heatmap
heatmap_data = element_avg.pivot(index='Element Label', columns='Location', values='Concentration')

# Plot heatmap
#learn how to create a dropdown menu to select the month and plot of the data for that month.
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="viridis", annot=True, fmt=".3f") # will help visualize data in 2D
plt.title('Average Concentration of Top Elements by Location', fontsize=14, fontweight='bold')
plt.ylabel('Element')
plt.xlabel('Location')
plt.tight_layout()
plt.savefig('TopSamplesbyLocation.png', dpi=300, bbox_inches='tight')
plt.show()

plt.figure(figsize=(14, 6))
sns.boxplot(data=all_data[all_data['Element Label'].isin(top_elements)],
            x='Element Label', y='Concentration')
plt.yscale('log')  # Use log scale if ranges vary a lot
plt.title('Variation in Element Concentrations Across All Locations and Months (Top 10 Elements)')
plt.xlabel('Element')
plt.ylabel('Concentration (ppm)')
plt.tight_layout()
plt.savefig('DistributionofElement.png', dpi=300, bbox_inches='tight')
plt.show()


# Filter for Thallium (Tl)
tl_data = all_data[all_data['Element Label'] == 'Tl'].copy()
# Remove DI samples and HNO
tl_data = tl_data[~tl_data['Lims ID'].str.contains('DI|HNO', case=False, na=False)]
# Extract base location name (remove trailing trial number)
# Cleans data; takes DI and DI&NO samples out of the data
tl_data['Location'] = tl_data['Lims ID'].str.extract(r'([A-Za-z\s]+)', expand=False).str.strip()
tl_data = tl_data[~tl_data['Lims ID'].str.contains('DI|HNO', case=False, na=False)]


# Average Thallium concentration for each location and month (ex: Average of 3 samples from Herndon in May)
tl_avg = tl_data.groupby(['Location', 'Month'])['Concentration'].mean().reset_index()
tl_avg_sorted = tl_avg.sort_values('Concentration', ascending=False)
sns.barplot(data=tl_avg_sorted, x='Location', y='Concentration')
plt.xlabel('Location', fontsize=10, fontweight='bold')
plt.ylabel('Average Concentration (ppm)', fontsize=10, fontweight='bold')
plt.title('Average Thallium Concentration by Location (Highest to Lowest)', fontsize=14, fontweight='bold')
sns.set(style='whitegrid')  # Options: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('TlLocation.png', dpi=300, bbox_inches='tight')
#Saves the plot as a PNG file


#Creating the bar plot for Average Thallium (Tl) Concentration by Location and Month
plt.figure(figsize=(12, 6)) #Creates a blank area for the plot and sets the figure to size
sns.barplot(data=tl_avg, x='Location', y='Concentration', hue='Month') #creates the bar plot, hue means the color of the column's category
plt.title('Average Thallium (Tl) Concentration by Location and Month', fontsize=16, fontweight='bold')
plt.xlabel('Location', fontsize=12, fontweight='bold')
plt.ylabel('Average Concentration (ppm)', fontsize=12, fontweight='bold')
plt.xticks(rotation=45)
plt.tight_layout()
sns.set(style='whitegrid')  # Options: 'darkgrid', 'whitegrid', 'dark', 'white', 'ticks'
plt.grid(axis='y', linestyle='--', alpha=0.7)
# Adding a horizontal line for EPA limit of Thallium (0.002 ppm)
epa_limit = 0.002
plt.axhline(y=epa_limit, color='red', linestyle='--', linewidth=1, label='EPA Limit (0.002 ppm)')
plt.legend()
plt.savefig('thallium_plot.png', dpi=300, bbox_inches='tight')
#Saves the plot as a PNG file
plt.show()




  