import matplotlib.pyplot as plt
import numpy as np

# Existing data
locations = ['Bangladesh', 'Bangladesh', 'Bangladesh', 'Morocco', 'Morocco', 'Morocco']
wc_value_type = ['WP', 'FC', 'SAT', 'WP', 'FC', 'SAT']
yield_rmse = [31.58560489, 31.58564166, 31.58570381, 2.166246648, 1.469644102, 1.471088931]
yield_rmse_percentage = [82.64908332, 82.64917953, 82.64934214, 101.3136894, 68.73412415, 68.80169772]

# New data for Water Used
Water_Used_RMSE = [382.3302148, 323.751363, 315.0857379, 52.18892805, 0, 0]
Water_Used_RMSE_percentage = [155.3638682, 131.5597411, 128.0383741, 32.09027938, 0, 0]

# Colors
colors = {
    'WP': (223/255, 122/255, 94/255),
    'FC': (130/255, 178/255, 154/255),
    'SAT': (242/255, 204/255, 142/255),
}

# Create subplots
fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(14, 6))

# Bar positions
bar_positions = [0, 0.4, 0.8, 2, 2.4, 2.8]

# Plot Yield RMSE
for wc_type in set(wc_value_type):
    wc_data_indices = [i for i, wc in enumerate(wc_value_type) if wc == wc_type]
    ax1.bar([bar_positions[i] for i in wc_data_indices], [yield_rmse[i] for i in wc_data_indices], width=0.35, align='center', label=f'{wc_type}', color=colors[wc_type], alpha=0.9)

# Labels and titles
ax1.set_title('Yield RMSE and Percentage RMSE by Initial Water Content')
ax1.set_ylabel('Yield RMSE')
ax1.set_xticks([0.4, 2.4])
ax1.set_xticklabels(['Bangladesh', 'Morocco'])
ax1.set_ylim(0, max(yield_rmse) * 1.2)

# Adding text labels
for i, pos in enumerate(bar_positions):
    ax1.text(pos, yield_rmse[i] + 1, f'{yield_rmse[i]:.2f}', ha='center', va='bottom', fontsize=10, color='black')

# Add second y-axis
ax2 = ax1.twinx()
ax2.plot(bar_positions, yield_rmse_percentage, marker='o', color=(60/255, 64/255, 91/255), label='Percentage RMSE')
ax2.set_ylabel('Yield Percentage RMSE')
ax2.set_ylim(0, max(yield_rmse_percentage) * 1.1)

# Adding labels to line plot data points
for i, (x, y) in enumerate(zip(bar_positions, yield_rmse_percentage)):
    ax2.text(x, y + 1, f'{y:.2f}', ha='center', va='bottom', fontsize=10, color='black')

# Plot for Water Used RMSE
for wc_type in set(wc_value_type):
    wc_data_indices = [i for i, wc in enumerate(wc_value_type) if wc == wc_type]
    ax3.bar([bar_positions[i] for i in wc_data_indices], [Water_Used_RMSE[i] for i in wc_data_indices], width=0.35, align='center', label=f'{wc_type}', color=colors[wc_type], alpha=0.9)

# Labels and titles
ax3.set_title('Water Used RMSE and Percentage RMSE by Initial Water Content')
ax3.set_ylabel('Water Used RMSE')
ax3.set_xticks([0.4, 2.4])
ax3.set_xticklabels(['Bangladesh', 'Morocco'])
ax3.set_ylim(0, max(Water_Used_RMSE) * 1.2)

# Adding text labels
for i, pos in enumerate(bar_positions):
    ax3.text(pos, Water_Used_RMSE[i] + 1, f'{Water_Used_RMSE[i]:.2f}', ha='center', va='bottom', fontsize=10, color='black')

# Add second y-axis
ax4 = ax3.twinx()
ax4.plot(bar_positions, Water_Used_RMSE_percentage, marker='o', color=(60/255, 64/255, 91/255), label='Water Used Percentage RMSE')
ax4.set_ylabel('Water Used Percentage RMSE')
ax4.set_ylim(0, max(Water_Used_RMSE_percentage) * 1.1)

# Adding labels to line plot data points
for i, (x, y) in enumerate(zip(bar_positions, Water_Used_RMSE_percentage)):
    ax4.text(x, y + 1, f'{y:.2f}', ha='center', va='bottom', fontsize=10, color='black')

# Add legends
ax1.legend(title='Initial Water Content type', loc='upper right',)
ax2.legend(loc='upper left')
ax3.legend(title='Initial Water Content type', loc='upper right')
ax4.legend(loc='upper left')

plt.tight_layout()
plt.show()
