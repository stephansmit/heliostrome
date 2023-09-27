import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
excel_file = r'heliostrome\jip_project\results\test_results.xlsx'
sheet_name = "Output Results"
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Group the data by 'Case Study' and calculate the average 'Yield (tonne/ha)'
average_yields = df.groupby('Case Study')['Yield (tonne/ha)'].mean().reset_index()
experimental_yields = pd.read_excel(excel_file, sheet_name="Input Parameters")

graphing_dataframe = pd.merge(experimental_yields[['Case Study', 'Yield (Ton/HA)']], average_yields[['Case Study', 'Yield (tonne/ha)']])

# Create the bar chart
X_axis = np.arange(len(graphing_dataframe['Case Study']))

ax = graphing_dataframe.plot(kind='bar', x='Case Study', figsize=(10, 6))

ax.bar(X_axis - 0.2, graphing_dataframe['Yield (Ton/HA)'], 0.4, label='Expected Output')
ax.bar(X_axis + 0.2, graphing_dataframe['Yield (tonne/ha)'], 0.4, label='Actual Output')

plt.xlabel('Case Study')
plt.ylabel('Average Yield (tonne/ha)')
plt.title('Average Yield by Case Study')
plt.xticks(rotation=90)

# Add legend with appropriate labels
plt.legend(['Expected Output', 'Actual Output'])

plt.tight_layout()
plt.show()
