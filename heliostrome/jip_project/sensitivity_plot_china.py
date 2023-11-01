import matplotlib.pyplot as plt
import numpy as np

# New data for China
wc_values = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
yield_rmse = [2.609466869, 2.557536141, 2.629815189, 2.753928509, 2.866994324, 2.98273098, 3.056935488, 3.10946281, 3.149624626, 3.179256683]
yield_rmse_percentage = [23.22967539, 22.76738405, 23.41081771, 24.51568405, 25.52220466, 26.55250131, 27.21307556, 27.68067783, 28.03820142, 28.30198828]

# Create subplots
fig, ax = plt.subplots(figsize=(8, 6))

# Plot Yield RMSE with the specified color
ax.bar(wc_values, yield_rmse, width=3, align='center', label='Yield RMSE', color=(223/255, 122/255, 94/255), alpha=0.7)

# Labels and titles
ax.set_title('Yield RMSE and Percentage RMSE for Northeast China')
ax.set_xlabel('Initial Water Content Percentage')
ax.set_ylabel('RMSE')
ax.set_ylim(0, max(yield_rmse) * 1.2)

# Adding text labels
for i, value in enumerate(wc_values):
    ax.text(value, yield_rmse[i] + 0.1, f'{yield_rmse[i]:.2f}', ha='center', va='bottom', fontsize=10, color='black')

# Add second y-axis
ax2 = ax.twinx()
# Plot Yield RMSE Percentage with the specified color
ax2.plot(wc_values, yield_rmse_percentage, marker='o', color=(60/255, 64/255, 91/255), label='Percentage RMSE')

# Adding labels to line plot data points
for i, (x, y) in enumerate(zip(wc_values, yield_rmse_percentage)):
    ax2.text(x, y + 0.1, f'{y:.2f}', ha='center', va='bottom', fontsize=10, color='black')

# Add legends with adjusted positions
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines + lines2, labels + labels2, loc='upper left', bbox_to_anchor=(0.01, 0.99))

plt.tight_layout()
plt.show()
