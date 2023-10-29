import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np


def convert_Qlpm(df, field_size=None):

    # Create a new DataFrame to store the results
    new_df = pd.DataFrame()

    #convert pump flow from hourly to daily avg
    df_daily = df.groupby(df.index.date).mean()

    # Convert AVG liters per minute per day to cubic meters per day
    liters_per_min_to_cubic_meters_per_day = 1 / 1000  # 1 liter = 0.001 cubic meters
    minutes_in_a_day = 1440  # 24 hours * 60 minutes
    
    # Apply the conversion to the "Qlpm" column
    
    new_df["cubic_meters_per_day"] = df_daily["Qlpm"] * liters_per_min_to_cubic_meters_per_day * minutes_in_a_day
    new_df["Date"] = df_daily.index
     
    # If a field size (in hectares) is provided, calculate water depth in mm 
    # #(which is still related to that field size, but can be compared with general mm from aquacrop)
    if field_size is not None:
        
        # Calculate water depth in mm
        # # mm depth available for the field_size, not the same as aquacrop output, which is unrelated to fieldsize, but still comparable because of that
        new_df["Water_depth_mm"] = new_df["cubic_meters_per_day"] * 1000 / field_size

    return new_df



# def pump_compatibility(waterflux_excel_path, pump_df_path):
#     """Match up the datetime in the "Date" column from waterflux_excel and pump_df to align the Date column entries.
#     Compare "IrrDay" values of waterflux_excel with "Water_depth_mm" from pump_df.
#     If "IrrDay" > "Water_depth_mm," show those instances (date, IrrDay, Water_depth_mm) and indicate a message that the pump is not enough for irrigation."""

#     # Read the Excel files into DataFrames
#     waterflux_excel = pd.read_excel(waterflux_excel_path)
#     pump_df = pd.read_excel(pump_df_path)

#     # Extract the month and day from the "Date" column of waterflux
#     waterflux_excel['Month_Day'] = waterflux_excel['Date'].dt.strftime('%m-%d')
#     print(waterflux_excel)
#     # Extract the month and day from the "Date" column of pump_df
#     pump_df['Month_Day'] = pump_df['Date'].dt.strftime('%m-%d')

#     # Merge the DataFrames based on matching month and day
#     merged_df = pd.merge(waterflux_excel, pump_df, on="Month_Day", how="inner")
    
#     # Filter instances where "IrrDay" is greater than both "Pump 1" and "Pump 2"
#     insufficient_pump_df = merged_df[(merged_df["IrrDay"] > merged_df["Pump 1"])]
#     pd.set_option('display.max_rows', None)
#     print(merged_df)
#     if insufficient_pump_df.empty:
#         print("The pump is sufficient for irrigation for all available dates.")
#     else:
#         print("The pump may not be sufficient for irrigation on the following dates:")
#         print(insufficient_pump_df[["Date_x", "IrrDay", "Pump 1"]])

#     merged_df["Date_x"] = merged_df["Date_x"].dt.strftime('%d/%m/%Y')
    
#     # Your existing code to load data and create a figure
#     plt.figure(figsize=(12, 6))

#     # Define bar width and separation
#     bar_width = 0.4
#     bar_sep = 0.2

#     # Calculate the x-coordinates for each bar group
#     x = np.arange(len(merged_df["Date_x"]))
#     x1 = x - bar_sep
#     x2 = x + bar_sep

#     # Create bar plots with adjusted x-coordinates
#     plt.bar(x1, merged_df["IrrDay"], width=bar_width, label="Aquacrop Irrigation")
#     plt.bar(x2, merged_df["Pump 1"], width=bar_width, label="Pump 1")

#     # Other plot settings
#     plt.xlabel("Date")
#     plt.ylabel("Values")
#     plt.title("Aquacrop Irrigation vs Pump Potential")
#     plt.legend()
#     plt.xticks(x, merged_df["Date_x"], rotation=90)
#     plt.show()

#     return merged_df

def pump_compatibility(waterflux_excel_path, pump_df_path):
    """Match up the datetime in the "Date" column from waterflux_excel and pump_df to align the Date column entries.
    Compare "IrrDay" values of waterflux_excel with "Water_depth_mm" from pump_df.
    If "IrrDay" > "Water_depth_mm," show those instances (date, IrrDay, Water_depth_mm) and indicate a message that the pump is not enough for irrigation."""

    # Read the Excel files into DataFrames
    waterflux_excel = pd.read_excel(waterflux_excel_path)
    pump_df = pd.read_excel(pump_df_path)

    
    # Extract day and month from the "Date" column while ignoring the year
    waterflux_excel['Date (no year)'] = waterflux_excel['Date'].dt.strftime('%m-%d')
    pump_df['Date (no year)'] = pump_df['Date'].dt.strftime('%m-%d')

    # Calculate the average values for each day/month
    avg_df_waterflux = waterflux_excel.groupby('Date (no year)')['IrrDay'].mean().reset_index()
    avg_pump_df = pump_df.groupby('Date (no year)')['Pump 1'].mean().reset_index()

    # Merge the DataFrames
    merged_data = pd.merge(avg_df_waterflux, avg_pump_df, on="Date (no year)", how="inner")

    # Create a datetime index with an arbitrary year (e.g., 2005)
    merged_data['Date'] = pd.to_datetime('2005-' + merged_data['Date (no year)'])
    merged_data.set_index('Date', inplace=True)
    #merged_data.drop('Date (no year)', axis=1, inplace=True)
    
    print(f"raw merged data = \n{merged_data}")
    
    #resample based on weeks, shows date of last day in the summed week. 
    # #This does make some times stamps not contain a full week (first date point is a sunday, so first week only contains a sunday) or be outside of the original data dates (last date is a monday, so last week contains monday but goes to sunday, a guess)
    Weekly = merged_data.resample('W').sum()
    
    
    
    #clean the df from rows that have been added by resampling (dead data points)
    # if either "IrrDay" or "Pump 1" is not zero, the row will be included in the new DataFrame.
    Weekly = Weekly.loc[(Weekly['IrrDay'] != 0) | (Weekly['Pump 1'] != 0)]
    Weekly['Date'] = Weekly.index.date
    Weekly['Date'] = pd.to_datetime(Weekly['Date'])
    Weekly['Date (no year)'] = Weekly['Date'].dt.strftime('%m-%d')
    print(f"Weekly sampled data= \n{Weekly}")

    # Filter instances where "IrrDay" is greater than both "Pump 1" and "Pump 2"
    insufficient_pump_df = Weekly[(Weekly["IrrDay"] > Weekly["Pump 1"])]
    pd.set_option('display.max_rows', None)
    
    if insufficient_pump_df.empty:
        print("The pump is sufficient for irrigation for all available dates.")
    else:
        print("The pump may not be sufficient for irrigation on the following dates:")
        print(insufficient_pump_df[["IrrDay", "Pump 1"]])
    
    # Your existing code to load data and create a figure
    plt.figure(figsize=(16, 6))

    # Define bar width and separation
    bar_width = 0.4
    bar_sep = 0.2

    # Calculate the x-coordinates for each bar group
    x = np.arange(len(Weekly["Date"]))
    x1 = x - bar_sep
    x2 = x + bar_sep

    # Create bar plots with adjusted x-coordinates
    plt.bar(x1, Weekly["IrrDay"], width=bar_width, label="Aquacrop Irrigation")
    plt.bar(x2, Weekly["Pump 1"], width=bar_width, label="Pump 1")

    # Other plot settings
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.title("Aquacrop Irrigation vs Pump Potential")
    plt.legend()
    plt.xticks(x, Weekly["Date (no year)"], rotation=90)
    plt.show()

    return Weekly

""" the merging of the pump_df data with the waterflux data is repeated for each year in the waterflux data. 
The merging is based on matching month and day values, and since you are using an "inner" merge, 
only the rows with matching month and day values will be included in the result. This means that 
for each unique month and day in the waterflux data, corresponding rows from the pump_df will be 
included, and this process is repeated for each year in the waterflux data.

So, if the waterflux data spans 10 years, the merging process will consider matching month and day
 values for each of those 10 years in the waterflux data. The result will include data from the pump_df for each year, 
 as long as there are matching month and day values."""

def pump_solar_voltage_current_plot(voltage_pump,current_pump,voltage_solar,current_solar):
     fig, ax = plt.subplots()
     ax.plot(voltage_pump, current_pump, label="Pump")
     ax.plot(voltage_solar, current_solar, label="Solar")
     ax.set_xlabel("Voltage [V]")
     ax.set_ylabel("Current [A]")
     ax.legend()
     plt.show()
    
def pump_solar_voltage_power_plot(voltage_pump,power_pump,voltage_solar,power_solar):
    fig, ax = plt.subplots()
    ax.plot(voltage_pump, power_pump, label="Pump")
    ax.plot(voltage_solar, power_solar, label="Solar")
    ax.set_xlabel("Voltage [V]")
    ax.set_ylabel("Power [W]")
    ax.legend()
    plt.show()
