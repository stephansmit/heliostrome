# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# # Read the Excel file
# excel_file = r'heliostrome\jip_project\results\test_results_Bangladesh.xlsx'
# sheet_name = "Output Results"
# df = pd.read_excel(excel_file, sheet_name=sheet_name)

# # Group the data by 'Case Study' and calculate the average 'Yield (tonne/ha)' and standard deviation
# average_yields = df.groupby('Case Study')['Yield (tonne/ha)'].mean().reset_index()
# std_yields = df.groupby('Case Study')['Yield (tonne/ha)'].std().reset_index()
# experimental_yields = pd.read_excel(excel_file, sheet_name="Input Parameters")

# # Calculate the Mean Bias Error (MBE) in percentage
# merged_df = pd.merge(experimental_yields[['Case Study', 'Yield (Ton/HA)']], average_yields[['Case Study', 'Yield (tonne/ha)']], on='Case Study')
# merged_df['MBE'] = ((merged_df['Yield (tonne/ha)'] - merged_df['Yield (Ton/HA)']) / merged_df['Yield (Ton/HA)']) * 100

# graphing_dataframe = pd.merge(experimental_yields[['Case Study', 'Yield (Ton/HA)']], average_yields[['Case Study', 'Yield (tonne/ha)']])

# # Create the bar chart
# X_axis = np.arange(len(graphing_dataframe['Case Study']))

# ax = graphing_dataframe.plot(kind='bar', x='Case Study', figsize=(10, 6))

# ax.bar(X_axis - 0.2, graphing_dataframe['Yield (Ton/HA)'], 0.4, label='Expected Output')
# ax.bar(X_axis + 0.2, graphing_dataframe['Yield (tonne/ha)'], 0.4, label='Heliostrome Output')

# plt.xlabel('Case Study')
# plt.ylabel('Average Yield (tonne/ha)')
# plt.title('Average Yield by Case Study')
# plt.xticks(rotation=90)

# # Add legend with appropriate labels
# plt.legend(['Expected Output', 'Heliostrome Output'])

# plt.tight_layout()
# plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
excel_file = r'heliostrome\jip_project\results\test_results_Bangladesh.xlsx'
sheet_name = "Output Results"
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Group the data by 'Case Study' and calculate the average 'Yield (tonne/ha)' and standard deviation
average_yields = df.groupby('Case Study')['Yield (tonne/ha)'].mean().reset_index()
std_yields = df.groupby('Case Study')['Yield (tonne/ha)'].std().reset_index()
experimental_yields = pd.read_excel(excel_file, sheet_name="Input Parameters")

# Calculate the Mean Bias Error (MBE) in percentage
merged_df = pd.merge(experimental_yields[['Case Study', 'Yield (Ton/HA)']], average_yields[['Case Study', 'Yield (tonne/ha)']], on='Case Study')
merged_df['MBE'] = ((merged_df['Yield (tonne/ha)'] - merged_df['Yield (Ton/HA)']) / merged_df['Yield (Ton/HA)']) * 100

# Create a single DataFrame with Case Study as the index
graphing_dataframe = pd.merge(experimental_yields[['Case Study', 'Yield (Ton/HA)']], average_yields[['Case Study', 'Yield (tonne/ha)']])
graphing_dataframe.set_index('Case Study', inplace=True)

# Create a bar chart with crop yield, standard deviation, and MBE in the same graph
ax = graphing_dataframe.plot(kind='bar', figsize=(10, 6))

# Plot standard deviation as error bars
ax.errorbar(graphing_dataframe.index, graphing_dataframe['Yield (tonne/ha)'], yerr=std_yields['Yield (tonne/ha)'], fmt='o', label='Yield (tonne/ha)')

# Plot MBE as a line plot
ax.plot(graphing_dataframe.index, merged_df['MBE'], marker='o', color='r', label='MBE (%)')

plt.xlabel('Case Study')
plt.ylabel('Yield (tonne/ha)')
plt.title('Crop Yield, Standard Deviation, and Mean Bias Error(MBE)')
plt.xticks(rotation=90)

# Add legend with appropriate labels
plt.legend(['Yield (tonne/ha)', 'Standard Deviation', 'MBE (%)'])

plt.tight_layout()
plt.show()
