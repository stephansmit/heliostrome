import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the Excel file
excel_file = r"heliostrome\jip_project\results\test_results_Bangladesh.xlsx"
sheet_name = "Output Results"
df = pd.read_excel(excel_file, sheet_name=sheet_name)

# Group the data by 'Case Study' and calculate the average 'Yield (tonne/ha)'
average_yields = df.groupby("Case Study")["Yield (tonne/ha)"].mean().reset_index()
# std_yields = df.groupby('Case Study')['Yield (tonne/ha)'].std().reset_index()
experimental_yields = pd.read_excel(excel_file, sheet_name="Input Parameters")

# Calculate the Mean Bias Error (MBE) in percentage
merged_df = pd.merge(
    experimental_yields[["Case Study", "Yield (Ton/HA)"]],
    average_yields[["Case Study", "Yield (tonne/ha)"]],
    on="Case Study",
)
merged_df["MBE"] = (
    (merged_df["Yield (tonne/ha)"] - merged_df["Yield (Ton/HA)"])
    / merged_df["Yield (Ton/HA)"]
) * 100

# Create the bar chart with expected and actual outcomes, MBE, and error bars
X_axis = np.arange(len(merged_df["Case Study"]))

fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot expected field outcomes
ax1.bar(
    X_axis - 0.2,
    merged_df["Yield (Ton/HA)"],
    0.4,
    label="Expected Output",
    color="blue",
)
# Plot average simulated outcomes
ax1.bar(
    X_axis + 0.2,
    merged_df["Yield (tonne/ha)"],
    0.4,
    label="Heliostrome Output",
    color="orange",
)
# Add x-axis labels with rotation
plt.xticks(X_axis, merged_df["Case Study"], rotation=90)

# Create a second y-axis for MBE
ax2 = ax1.twinx()
ax2.plot(
    X_axis, merged_df["MBE"], linestyle="-", marker="o", color="red", label="MBE (%)"
)

# Set labels for both y-axes
ax1.set_ylabel("Yield (tonne/ha)")
ax2.set_ylabel("MBE (%)")

# Add legend with appropriate labels
ax1.legend(["Expected Output", "Avg Heliostrome Output"], loc="upper left")
ax2.legend(["MBE (%)"], loc="upper right")

plt.title("Crop Yield Comparison with Mean Bias Error (MBE)")
plt.xticks(rotation=90)

plt.tight_layout()
plt.show()
