import pandas as pd

def convert_Qlpm(df, field_size=None):
    # Convert liters per minute to cubic meters per day
    liters_per_min_to_cubic_meters_per_day = 1 / 1000  # 1 liter = 0.001 cubic meters
    minutes_in_a_day = 1440  # 24 hours * 60 minutes

    # Apply the conversion to the "Qlpm" column
    df["cubic_meters_per_day"] = df["Qlpm"] * liters_per_min_to_cubic_meters_per_day * minutes_in_a_day

    
    # If a field size (in hectares) is provided, calculate water depth in mm 
    # #(which is still related to that field size, but can be compared with general mm from aquacrop)
    if field_size is not None:
        #convert ha to m2
        field_size_sqm = field_size * 10000
        # Calculate water depth in mm
        # # mm depth available for the field_size, not the same as aquacrop output, which is unrelated to fieldsize, but still comparable because of that
        df["Water_depth_mm"] = df["Volume_cubic_meters_per_day"] * 1000 / field_size_sqm 

    return df[["Volume_cubic_meters_per_day", "Water_depth_mm"]]

    


