import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from aquaplan_extractor import aquaplan_data

# Read the Excel file
excel_file = r"heliostrome\jip_project\results\test_results_northeastCHINA.xlsx"
sheet_name = "Output Results"
df = pd.read_excel(excel_file, sheet_name=sheet_name)
aquaplan_df = aquaplan_data()

# Group the data by 'Case Study' and calculate the average 'Yield (tonne/ha)'
average_yields = df.groupby("Case Study")["Yield (tonne/ha)"].mean().reset_index()
std_yields = df.groupby("Case Study")["Yield (tonne/ha)"].std().reset_index()
experimental_yields = pd.read_excel(excel_file, sheet_name="Input Parameters")

graphing_dataframe = pd.merge(
    experimental_yields[["Case Study", "Yield (Ton/HA)"]],
    average_yields[["Case Study", "Yield (tonne/ha)"]],
)
graphing_dataframe = pd.merge(
    graphing_dataframe, aquaplan_df, on="Case Study", how="left"
)
graphing_dataframe["MBE"] = (
    (graphing_dataframe["Yield (tonne/ha)"] - graphing_dataframe["Yield (Ton/HA)"])
    / graphing_dataframe["Yield (Ton/HA)"]
) * 100

CaseStudy_Names = [
    "Mulched + Drip - 2013",
    "Non-Mulched + Drip - 2013",
    "Mulched + Drip - 2014",
    "Non-Mulched + Drip - 2014",
    "Mulched + Rainfed - 2016",
    "Non-Mulched + Rainfed - 2016",
]

graphing_dataframe["Case Study"] = CaseStudy_Names

# Create the bar chart
X_axis = np.arange(len(graphing_dataframe["Case Study"]))

fig, ax1 = plt.subplots(figsize=(10, 6))

# ax1 = graphing_dataframe.plot(kind='bar', x='Case Study', figsize=(10, 6))

ax1.bar(
    X_axis - 0.2, graphing_dataframe["Yield (Ton/HA)"], 0.2, label="Heliostrome Output"
)
ax1.bar(
    X_axis,
    graphing_dataframe["Yield (tonne/ha)"],
    0.2,
    label="Expected Output",
    yerr=std_yields["Yield (tonne/ha)"],
    capsize=5,
)
ax1.bar(X_axis + 0.2, graphing_dataframe["Average_Yield"], 0.2, label="Aquaplan Output")

ax2 = ax1.twinx()
ax2.plot(
    X_axis,
    graphing_dataframe["MBE"],
    linestyle="-",
    marker="o",
    color="red",
    label="MBE (%)",
)

# Set labels for both y-axes
ax1.set_ylabel("Yield (tonne/ha)")
ax2.set_ylabel("MBE (%)")

# Set limits to y axis of MBE for scaling purposes
# ax2.set_ylim(0, 100)

# # Add legend with appropriate labels
# ax1.legend(['Expected Output', 'Heliostrome Output', 'Aquaplan Output'], loc='upper left')
# ax2.legend(['MBE (%)'], loc='upper right')

ax1.legend(
    ["Expected Output", "Heliostrome Output", "Aquaplan Output"],
    bbox_to_anchor=(1.05, 1),
    loc="upper left",
)
ax2.legend(["MBE (%)"], bbox_to_anchor=(1.05, 0), loc="lower left")

plt.xlabel("Case Study")
# plt.ylabel('Average Yield (tonne/ha)')
plt.title("Average Yield as a function of irrigation method & mulch application")
plt.xticks(rotation=90)

# Add legend with appropriate labels
# plt.legend(['Expected Output', 'Heliostrome Output', 'Aquaplan Output'])

plt.tight_layout()
plt.show()

# def percentage_error(list1, list2):
#     if len(list1) != len(list2):
#         raise ValueError("Both lists must have the same length")

#     errors = []

#     for val1, val2 in zip(list1, list2):
#         if val1 == 0:
#             error = 0  # Avoid division by zero
#         else:
#             error = ((val2 - val1) / val1) * 100
#         errors.append(error)

#     return errors

# experimental_simulation_yield = [9.4,9.6,13.6,12,9.2,9.4]
# experimental_simulation_error = percentage_error(graphing_dataframe['Yield (Ton/HA)'], experimental_simulation_yield)
# experimental_heliostrome_error = percentage_error(graphing_dataframe['Yield (Ton/HA)'],graphing_dataframe['Yield (tonne/ha)'])
# experiental_aquaplan_error = percentage_error(graphing_dataframe['Yield (Ton/HA)'],graphing_dataframe['Average_Yield'])

# error_data = {
#     'Case Study': ['Mulched + Drip - 2013', 'Non-Mulche d + Drip - 2013', 'Mulched + Drip - 2014', 'Non-Mulched + Drip - 2014','Mulched + Rainfed - 2016','Non-Mulched + Rainfed - 2016'],
#     'experimental_simulation_error': experimental_simulation_error,
#     'experimental_heliostrome_error': experimental_heliostrome_error,
#     'experiental_aquaplan_error': experiental_aquaplan_error
# }

# # Create a DataFrame from the dictionary
# error_df = pd.DataFrame(error_data)


# X_axis = np.arange(len(graphing_dataframe['Case Study']))

# ax = error_df.plot(kind='bar', x='Case Study', figsize=(10, 6))

# ax.bar(X_axis - 0.2, error_df['experimental_simulation_error'], 0.2, label='Experimental - Case Study Simulation Error')
# ax.bar(X_axis, error_df['experimental_heliostrome_error'], 0.2, label='Experimental - Heliostrome Error')
# ax.bar(X_axis + 0.2, error_df['experiental_aquaplan_error'], 0.2, label='Experimental - Aquaplan Error')


# plt.xlabel('Case Study')
# plt.ylabel('Percentage Error of Yield (%)')
# plt.title('Percentage Error of various modelling methods to determine the yield of maize in northern China')
# plt.xticks(rotation=90)

# # Add legend with appropriate labels
# plt.legend(['Experimental - Case Study Simulation Error', 'Experimental - Heliostrome Error', 'Experimental - Aquaplan Error'])

# plt.tight_layout()
# plt.show()
