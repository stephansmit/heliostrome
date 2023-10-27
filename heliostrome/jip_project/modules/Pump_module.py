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



def pump_compatibility(waterflux_excel, pump_df):
    """Match up the datetime in the "Date" column from waterflux_excel and pump_df to align the Date column entries.
    Compare "IrrDay" values of waterflux_excel with "Water_depth_mm" from pump_df.
    If "IrrDay" > "Water_depth_mm," show those instances (date, IrrDay, Water_depth_mm) and indicate a message that the pump is not enough for irrigation."""

    # Extract the month/day from the "Date" column of pump_df
    pump_df['Date'] = pump_df['Date'].dt.strftime('%m/%d')

    # Merge the two DataFrames on the "Date" column (month/day)
    merged_df = pd.merge(waterflux_excel, pump_df, on="Date", how="inner")

    # Filter instances where "IrrDay" is greater than "Water_depth_mm"
    insufficient_pump_df = merged_df[merged_df["IrrDay"] > merged_df["Water_depth_mm"]]

    if insufficient_pump_df.empty:
        print("The pump is sufficient for irrigation for all available dates.")
    else:
        print("The pump may not be sufficient for irrigation on the following dates:")
        print(insufficient_pump_df[["Date", "IrrDay", "Water_depth_mm"]])

    # Create a bar plot of "IrrDay" and "Water_depth_mm" against "Date"
    plt.figure(figsize=(12, 6))
    plt.bar(merged_df["Date"], merged_df["IrrDay"], label="Aquacrop Irrigation")
    plt.bar(merged_df["Date"], merged_df["Water_depth_mm"], label="Pump Potential")
    plt.xlabel("Date (Month/Day)")
    plt.ylabel("Values")
    plt.title("Aquacrop Irrigation vs Pump Potential")
    plt.legend()
    plt.xticks(rotation=45)
    plt.show()

    return merged_df
