import pandas as pd
import matplotlib.pyplot as plt
import random


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

  




# def pump_compatibility(waterflux_excel, Daily_Pump_data):
#     """Match up the datetime in the "Date" column from clean_excel_file and pump_df to align the Date column entries. 
#     Compare "IrrDay" values of clean_excel with "Water_depth_mm" from pump_df. 
#     If "IrrDay" > "Water_depth_mm," show those instances (date, IrrDay, Water_depth_mm) and indicate a message that the pump is not enough for irrigation."""

#     # Merge the two DataFrames on the "Date" column
#     merged_df = pd.merge(waterflux_excel, Daily_Pump_data, on="Date", how="inner")

#     # Filter instances where "IrrDay" is greater than "Water_depth_mm"
#     insufficient_pump_df = merged_df[merged_df["IrrDay"] > merged_df["Water_depth_mm"]]

#     if insufficient_pump_df.empty:
#         print("The pump is sufficient for irrigation for all available dates.")
#     else:
#         print("The pump may not be sufficient for irrigation on the following dates:")
#         print(insufficient_pump_df[["Date", "IrrDay", "Water_depth_mm"]])
    
    
#     # Create a bar plot of "IrrDay" and "Water_depth_mm" against date
#     plt.figure(figsize=(12, 6))
#     plt.bar(merged_df["Date"], merged_df["IrrDay"], label="Aquacrop Irrigation")
#     plt.bar(merged_df["Date"], merged_df["Water_depth_mm"], label="Pump Potential")
#     plt.xlabel("Date")
#     plt.ylabel("Values")
#     plt.title("Aquacrop Irrigation vs Pump Potential")
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.show()

#     return merged_df



# def pump_compatibility(waterflux_excel_path, pump_df_path):
#     """Match up the datetime in the "Date" column from waterflux_excel and pump_df to align the Date column entries.
#     Compare "IrrDay" values of waterflux_excel with "Water_depth_mm" from pump_df.
#     If "IrrDay" > "Water_depth_mm," show those instances (date, IrrDay, Water_depth_mm) and indicate a message that the pump is not enough for irrigation."""

#     # Read the Excel files into DataFrames
#     waterflux = pd.read_excel(waterflux_excel_path)
#     pump_df = pd.read_excel(pump_df_path)

#     # Convert the "Date" column in pump_df to datetime
#     pump_df['Date'] = pd.to_datetime(pump_df['Date'])

#     # Extract the month/day from the "Date" column of pump_df
#     pump_df['Date'] = pump_df['Date'].dt.strftime('%m/%d')

#     # Merge the two DataFrames on the "Date" column (month/day)
#     merged_df = pd.merge(waterflux, pump_df, on="Date", how="inner")

#     # Filter instances where "IrrDay" is greater than "Water_depth_mm"
#     insufficient_pump_df = merged_df[merged_df["IrrDay"] > merged_df["Water_depth_mm"]]

#     if insufficient_pump_df.empty:
#         print("The pump is sufficient for irrigation for all available dates.")
#     else:
#         print("The pump may not be sufficient for irrigation on the following dates:")
#         print(insufficient_pump_df[["Date", "IrrDay", "Water_depth_mm"]])

#         # Create a bar plot of "IrrDay" and "Water_depth_mm" against "Date"
#     plt.figure(figsize=(12, 6))
#     plt.bar(merged_df["Date"], merged_df["IrrDay"], label="Aquacrop Irrigation")
#     plt.bar(merged_df["Date"], merged_df["Water_depth_mm"], label="Pump Potential")
#     plt.xlabel("Date (Month/Day)")
#     plt.ylabel("Values")
#     plt.title("Aquacrop Irrigation vs Pump Potential")
#     plt.legend()
#     plt.xticks(rotation=45)
#     plt.show()

#     return merged_df



def pump_compatibility(waterflux_excel_path, pump_df_path):
    """Match up the datetime in the "Date" column from waterflux_excel and pump_df to align the Date column entries.
    Compare "IrrDay" values of waterflux_excel with "Water_depth_mm" from pump_df.
    If "IrrDay" > "Water_depth_mm," show those instances (date, IrrDay, Water_depth_mm) and indicate a message that the pump is not enough for irrigation."""

    # Read the Excel files into DataFrames
    waterflux_excel = pd.read_excel(waterflux_excel_path)
    pump_df = pd.read_excel(pump_df_path)

    # Extract the month and day from the "Date" column of waterflux
    waterflux_excel['Month_Day'] = waterflux_excel['Date'].dt.strftime('%m-%d')

    # Extract the month and day from the "Date" column of pump_df
    pump_df['Month_Day'] = pump_df['Date'].dt.strftime('%m-%d')

    # Merge the DataFrames based on matching month and day
    merged_df = pd.merge(waterflux_excel, pump_df, on="Month_Day", how="inner")

    # Filter instances where "IrrDay_waterflux" is greater than "Water_depth_mm_pump"
    insufficient_pump_df = merged_df[merged_df["IrrDay_waterflux"] > merged_df["Water_depth_mm_pump"]]

    if insufficient_pump_df.empty:
        print("The pump is sufficient for irrigation for all available dates.")
    else:
        print("The pump may not be sufficient for irrigation on the following dates:")
        print(insufficient_pump_df[["Date_waterflux", "IrrDay_waterflux", "Water_depth_mm_pump"]])

    # Create a bar plot of "IrrDay" and "Water_depth_mm" against "Date"
    plt.figure(figsize=(12, 6))
    plt.bar(merged_df["Date_waterflux"], merged_df["IrrDay_waterflux"], label="Aquacrop Irrigation")
    plt.bar(merged_df["Date_waterflux"], merged_df["Water_depth_mm_pump"], label="Pump Potential")
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.title("Aquacrop Irrigation vs Pump Potential")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    return merged_df

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
