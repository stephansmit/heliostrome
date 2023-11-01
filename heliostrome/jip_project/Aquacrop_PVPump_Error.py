from modules.waterflux_extraction import *
from modules.Pump_module import *
import pandas as pd
import matplotlib.pyplot as plt


waterfluxexcelpath = r'heliostrome\jip_project\results\cleaned_WaterFlux_Bangladesh.xlsx'
pump_df_path = r'heliostrome\jip_project\results\PVPUmp_Data.xlsx'
output_file_path = 'heliostrome\\jip_project\\results\\pump_compatibility\\'
 #csv location

merged_df = pump_compatibility(waterfluxexcelpath, pump_df_path, output_file_path)

###CSV Inputs
mpe_df_avg_list = []
error_df = pd.DataFrame()

for i in range (13,18):
    csv_pump_file = r'heliostrome\jip_project\results\pump_compatibility\_Pump ' + str(i+1) + '.csv'
    df = pd.read_csv(csv_pump_file)
    mpe_indiv, mpe_df_avg = mean_percentage_error(df,'Pump',df,'IrrDay')
    column_name = 'Setup ' + str(i+1)
    error_df[column_name] = mpe_indiv.iloc[1:]
    mpe_df_avg_list.append(mpe_df_avg)
    lower_bound = -20
    upper_bound = 20

    # Create boolean masks to identify values outside the range for each column
    threshold_check = (mpe_indiv < lower_bound) | (mpe_indiv > upper_bound)

    # Count the occurrences of values outside the range for each column
    threshold_count = threshold_check.sum()
    print(threshold_count)

df['Date'] = pd.to_datetime(df['Date'])
error_df.insert(0, 'Date', df['Date'].apply(lambda x: x.strftime("%b %d")))

colors = ['b', 'g', 'r', 'c', 'm']  # Define the colors for each set of three columns
line_styles = ['-', '--', '-.']  # Line styles for each column within a set

columns_to_plot = error_df.columns[1:]
labels = ['4,1','5,1','6,1','2,2','3,2']

# Create a line plot for each selected column (solar panel)
# for i, column in enumerate(columns_to_plot):
#     color = colors[i // 1 % len(colors)]  # Cycle through the colors every three columns
#     #line_style = line_styles[i % 3]  # Cycle through the line styles
#     plt.plot(error_df['Date'], error_df[column], label=labels[i], color=color)

# Create a line plot for each selected column (everything)
for i, column in enumerate(columns_to_plot):
    color = colors[i // 3 % len(colors)]  # Cycle through the colors every three columns
    line_style = line_styles[i % 3]  # Cycle through the line styles
    plt.plot(error_df['Date'], error_df[column], label=labels[i], color=color, linestyle=line_style)
    
# Add labels and legend
plt.xlabel('Date')
plt.ylabel('Mean Percentage Error (%)')
plt.title('Variation of error in SPIS sizing as a function of the number of solar panel modules')
plt.legend()
plt.xticks(rotation=90)

# Show the plot
plt.show()

print(mpe_df_avg_list)
# waterflux_df = pd.read_excel(waterfluxexcelpath)
# pump_df = pd.read_excel(pump_df_path)

