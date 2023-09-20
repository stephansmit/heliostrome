import pandas as pd
import matplotlib.pyplot as plt

# Read the Excel file
excel_file = r'heliostrome\jip_project\results\test_results.xlsx'
sheet_name = "Output Results"
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Group the data by 'Case Study' and calculate the average 'Yield (tonne/ha)'
average_yields = df.groupby('Case Study')['Yield (tonne/ha)'].mean().reset_index()
print(average_yields)
# Create the bar chart
plt.figure(figsize=(10, 6))  # Adjust the figure size as needed
plt.bar(average_yields['Case Study'], average_yields['Yield (tonne/ha)'])
plt.xlabel('Case Study')
plt.ylabel('Average Yield (tonne/ha)')
plt.title('Average Yield by Case Study')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability if needed
plt.tight_layout()  # Ensure all labels are visible
plt.show()
