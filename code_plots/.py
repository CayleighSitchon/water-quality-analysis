# Example: Pivot to compare elements across locations
element_avg = all_data.groupby(['Element Label', 'Location'])['Concentration'].mean().reset_index()
heatmap_data = element_avg.pivot(index='Element Label', columns='Location', values='Concentration')

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="viridis", annot=True, fmt=".3f")
plt.title('Average Element Concentration by Location')
plt.ylabel('Element')
plt.xlabel('Location')
plt.tight_layout()
plt.show()
