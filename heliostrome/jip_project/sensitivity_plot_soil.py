import matplotlib.pyplot as plt
import numpy as np

# Existing data for soil type
locations = ["Bangladesh"] * 14
soil_type = [
    "Clay",
    "ClayLoam",
    "Loam",
    "LoamySand",
    "Sand",
    "SandyClay",
    "SandyClayLoam",
    "SandyLoam",
    "Silt",
    "SiltClayLoam",
    "SiltLoam",
    "SiltClay",
    "Paddy",
    "ac_TunisLocal",
]
yield_rmse = [
    38.75945715,
    31.58564166,
    31.58502913,
    31.58502365,
    31.58502365,
    31.59291301,
    31.58503875,
    31.58502365,
    31.5853929,
    31.58525588,
    31.58504707,
    34.4411245,
    35.70949357,
    31.71743356,
]
yield_rmse_percentage = [
    101.4206824,
    82.64917953,
    82.64757674,
    82.64756239,
    82.64756239,
    82.66820625,
    82.64760191,
    82.64756239,
    82.64852859,
    82.64817006,
    82.64762367,
    90.12103386,
    93.4399363,
    82.99403536,
]
water_used_rmse = [
    170.0926316,
    323.751363,
    332.3115709,
    341.3426932,
    337.650014,
    322.1579658,
    326.4977306,
    345.0297398,
    332.9589972,
    324.344311,
    334.928779,
    252.2981169,
    230.7853976,
    318.6975205,
]
water_used_rmse_percentage = [
    69.11891392,
    131.5597411,
    135.0382709,
    138.7081615,
    137.2076029,
    130.9122476,
    132.6757562,
    140.2064314,
    135.3013593,
    131.8006918,
    136.1018006,
    102.5239698,
    93.78205201,
    129.5060596,
]

# Colors
colors = {
    "Clay": "red",
    "ClayLoam": "blue",
    "Loam": "green",
    "LoamySand": "purple",
    "Sand": "orange",
    "SandyClay": "pink",
    "SandyClayLoam": "brown",
    "SandyLoam": "cyan",
    "Silt": "magenta",
    "SiltClayLoam": "lime",
    "SiltLoam": "gray",
    "SiltClay": "olive",
    "Paddy": "navy",
    "ac_TunisLocal": "teal",
}

# Create subplots
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(14, 6))

# Bar positions
bar_positions = np.arange(len(locations))

# Plot Yield RMSE
for soil in set(soil_type):
    soil_data_indices = [i for i, s in enumerate(soil_type) if s == soil]
    ax1.bar(
        [bar_positions[i] for i in soil_data_indices],
        [yield_rmse[i] for i in soil_data_indices],
        width=0.35,
        align="center",
        label=f"{soil}",
        color=colors[soil],
        alpha=0.9,
    )

# Labels and titles
ax1.set_title("Yield RMSE and Percentage RMSE by Soil Type")
ax1.set_ylabel("Yield RMSE")
ax1.set_xticks(bar_positions)
ax1.set_xticklabels(locations, rotation=45, ha="right")
ax1.set_ylim(0, max(yield_rmse) * 1.2)

# Adding text labels
for i, pos in enumerate(bar_positions):
    ax1.text(
        pos,
        yield_rmse[i] + 1,
        f"{yield_rmse[i]:.2f}",
        ha="center",
        va="bottom",
        fontsize=10,
        color="black",
    )

# Add second y-axis
ax2 = ax1.twinx()
ax2.plot(
    bar_positions,
    yield_rmse_percentage,
    marker="o",
    color=(60 / 255, 64 / 255, 91 / 255),
    label="Percentage RMSE",
)
ax2.set_ylabel("Yield Percentage RMSE")
ax2.set_ylim(0, max(yield_rmse_percentage) * 1.1)

# Adding labels to line plot data points
for i, (x, y) in enumerate(zip(bar_positions, yield_rmse_percentage)):
    ax2.text(x, y + 1, f"{y:.2f}", ha="center", va="bottom", fontsize=10, color="black")

# Plot for Water Used RMSE
for soil in set(soil_type):
    soil_data_indices = [i for i, s in enumerate(soil_type) if s == soil]
    ax3.bar(
        [bar_positions[i] for i in soil_data_indices],
        [water_used_rmse[i] for i in soil_data_indices],
        width=0.35,
        align="center",
        label=f"{soil}",
        color=colors[soil],
        alpha=0.9,
    )

# Labels and titles
ax3.set_title("Water Used RMSE and Percentage RMSE by Soil Type")
ax3.set_ylabel("Water Used RMSE")
ax3.set_xticks(bar_positions)
ax3.set_xticklabels(locations, rotation=45, ha="right")
ax3.set_ylim(0, max(water_used_rmse) * 1.2)

# Adding text labels
for i, pos in enumerate(bar_positions):
    ax3.text(
        pos,
        water_used_rmse[i] + 1,
        f"{water_used_rmse[i]:.2f}",
        ha="center",
        va="bottom",
        fontsize=10,
        color="black",
    )

# Add second y-axis
ax4 = ax3.twinx()
ax4.plot(
    bar_positions,
    water_used_rmse_percentage,
    marker="o",
    color=(60 / 255, 64 / 255, 91 / 255),
    label="Water Used Percentage RMSE",
)
ax4.set_ylabel("Water Used Percentage RMSE")
ax4.set_ylim(0, max(water_used_rmse_percentage) * 1.1)

# Adding labels to line plot data points
for i, (x, y) in enumerate(zip(bar_positions, water_used_rmse_percentage)):
    ax4.text(x, y + 1, f"{y:.2f}", ha="center", va="bottom", fontsize=10, color="black")

# Add legends
ax1.legend(
    title="Soil Type",
    loc="upper right",
)
ax2.legend(loc="upper left")
ax3.legend(title="Soil Type", loc="upper right")
ax4.legend(loc="upper left")

plt.tight_layout()
plt.show()
