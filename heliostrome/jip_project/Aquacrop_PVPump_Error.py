from modules.waterflux_extraction import *
from modules.Pump_module import *
import pandas as pd
import matplotlib.pyplot as plt


waterfluxexcelpath = r'heliostrome\jip_project\results\cleaned_WaterFlux_Bangladesh.xlsx'
pump_df_path = r'heliostrome\jip_project\results\PVPUmp_Data.xlsx'
output_file_path = 'heliostrome\\jip_project\\results\\pump_compatibility\\'
 #csv location

# merged_df = pump_compatibility(waterfluxexcelpath, pump_df_path, output_file_path)

###CSV Inputs
mpe_df_avg_list = []
error_df = pd.DataFrame()

for i in range (15):
    csv_pump_file = r'heliostrome\jip_project\results\pump_compatibility\_Pump ' + str(i+1) + '.csv'
    df = pd.read_csv(csv_pump_file)
    mpe_indiv, mpe_df_avg = mean_percentage_error(df,'Pump',df,'IrrDay')
    column_name = 'Setup ' + str(i+1)
    error_df[column_name] = mpe_indiv
    mpe_df_avg_list.append(mpe_df_avg)
    
error_df.insert(0, 'Date', df['Date'])

colors = ['b', 'g', 'r', 'c', 'm']  # Define the colors for each set of three columns
line_styles = ['-', '--', '-.']  # Line styles for each column within a set

columns_to_plot = error_df.columns[1:]

# Create a line plot for each selected column
for i, column in enumerate(columns_to_plot):
    color = colors[i // 3 % len(colors)]  # Cycle through the colors every three columns
    line_style = line_styles[i % 3]  # Cycle through the line styles
    plt.plot(df['Date'], error_df[column], label=column, color=color, linestyle=line_style)

# for column in error_df.columns[1:]:
#     plt.plot(df['Date'], error_df[column], label=column)

# Add labels and legend
plt.xlabel('Date')
plt.ylabel('Mean Percentage Error')
plt.legend()

# Show the plot
plt.show()

# waterflux_df = pd.read_excel(waterfluxexcelpath)
# pump_df = pd.read_excel(pump_df_path)

