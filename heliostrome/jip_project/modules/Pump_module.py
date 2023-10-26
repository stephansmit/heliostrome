import pandas as pd
"""IMPARTANT needs pvps.flow data that as been converted to daily avg Qlpm!!! Field size in m2"""
def convert_Qlpm(df, field_size=None):

    # Create a new DataFrame to store the results
    new_df = pd.DataFrame()

    # Convert AVG liters per minute per day to cubic meters per day
    liters_per_min_to_cubic_meters_per_day = 1 / 1000  # 1 liter = 0.001 cubic meters
    minutes_in_a_day = 1440  # 24 hours * 60 minutes
    
    # Apply the conversion to the "Qlpm" column
    new_df["cubic_meters_per_day"] = df["Qlpm"] * liters_per_min_to_cubic_meters_per_day * minutes_in_a_day
    new_df["Date"] = df.index
     
    # If a field size (in hectares) is provided, calculate water depth in mm 
    # #(which is still related to that field size, but can be compared with general mm from aquacrop)
    if field_size is not None:
        
        # Calculate water depth in mm
        # # mm depth available for the field_size, not the same as aquacrop output, which is unrelated to fieldsize, but still comparable because of that
        new_df["Water_depth_mm"] = new_df["cubic_meters_per_day"] * 1000 / field_size

    return new_df

  

def pump_compatibility(waterflux_excel, pump_df):
    """Match up the datetime in the "Date" column from clean_excel_file and pump_df to align the Date column entries. 
    Compare "IrrDay" values of clean_excel with "Water_depth_mm" from pump_df. 
    If "IrrDay" > "Water_depth_mm," show those instances (date, IrrDay, Water_depth_mm) and indicate a message that the pump is not enough for irrigation."""

    # Merge the two DataFrames on the "Date" column
    merged_df = pd.merge(waterflux_excel, pump_df, on="Date", how="inner")

    # Filter instances where "IrrDay" is greater than "Water_depth_mm"
    insufficient_pump_df = merged_df[merged_df["IrrDay"] > merged_df["Water_depth_mm"]]

    if insufficient_pump_df.empty:
        print("The pump is sufficient for irrigation for all available dates.")
    else:
        print("The pump may not be sufficient for irrigation on the following dates:")
        print(insufficient_pump_df[["Date", "IrrDay", "Water_depth_mm"]])

# Example usage:
# pump_compatibility(waterflux_excel, pump_df)
