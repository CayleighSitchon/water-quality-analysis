import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# List of months / filenames you want to process
# These filenames should match the Excel files in your 'data' folder, e.g., 'Oct2024_Data.xlsx'
months = ['Oct2024', "Jan2025", "Feb2025", "March2025", "April2025", "Kern"]

# Create output directory if it doesn't exist
# Ensures the 'plots' folder exists so saving images won't cause an error
os.makedirs('plots', exist_ok=True)

# Loop through each month/file
for month in months:
    # Load monthly data from Excel file
    filepath = f'data/{month}_Data.xlsx'
    all_data = pd.read_excel(filepath)
    
    # Clean the 'Lims ID' column to remove irrelevant or bad rows
    all_data['Lims ID'] = all_data['Lims ID'].astype(str)  # Ensure Lims ID is string
    all_data = all_data[~all_data['Lims ID'].str.contains(r'\d+\.\d+', regex=True)]  # Remove IDs with decimal numbers (likely invalid)
    all_data = all_data[~all_data['Lims ID'].str.contains('DI|HNO', case=False, na=False)]  # Remove 'DI' or 'HNO' entries (likely blanks or acid blanks)

    # Extract location name from Lims ID using regex (pulls out letter/word-based names)
    all_data['Location'] = all_data['Lims ID'].str.extract(r'([A-Za-z\s]+)', expand=False).str.strip()

    # Convert the concentration column to numeric
    # Any errors (non-numeric entries) will become NaN
    all_data['Concentration'] = pd.to_numeric(all_data['Concentration'], errors='coerce')

    # Drop rows where Concentration is NaN (those couldn't be converted to numbers)
    all_data = all_data.dropna(subset=['Concentration'])

    # Get the top 10 elements with the highest average concentration in that month's dataset
    top_elements = (all_data.groupby('Element Label')['Concentration']
                    .mean()
                    .sort_values(ascending=False)
                    .head(10)
                    .index)

    # Filter dataset to only include rows for those top 10 elements
    filtered_data = all_data[all_data['Element Label'].isin(top_elements)]

    # Group by Element and Location, then calculate average concentration
    element_avg = (filtered_data.groupby(['Element Label', 'Location'])['Concentration']
                   .mean()
                   .reset_index())

    # Reshape the data into a pivot table for heatmap:
    # Rows = elements, Columns = locations, Values = average concentration
    heatmap_data = element_avg.pivot(index='Element Label', columns='Location', values='Concentration')

    # Create and customize the heatmap
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='viridis', annot=True, fmt=".3f")  # annot=True adds values, fmt=".3f" formats them to 3 decimals
    plt.title(f'Average Concentration of Top Elements by Location ({month})', fontsize=14, fontweight='bold')
    plt.ylabel('Element')
    plt.xlabel('Location')
    plt.tight_layout()  # Avoids label cutoff

    # Save heatmap plot to the 'plots' folder using the month in the filename
    plt.savefig(f'plots/TopElements_{month}_Heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to prevent memory leaks or overlapping plots

# Notify when done
print("Finished processing all months.")

from PIL import Image
import os

# Folder where plots are saved
plot_folder = 'plots'
# Get all heatmap images (ensure they are sorted by name/month if needed)
image_files = [f for f in os.listdir(plot_folder) if f.endswith('.png')]
image_files.sort()  # Optional: ensures they're in order

# Convert images to a list of PIL Image objects
images = [Image.open(os.path.join(plot_folder, f)).convert('RGB') for f in image_files]

# Save all images into one PDF
if images:
    images[0].save("WaterQuality_Report.pdf", save_all=True, append_images=images[1:])
    print("PDF report created: WaterQuality_Report.pdf")
else:
    print("No heatmap images found to include in the report.")
