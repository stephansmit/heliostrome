# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np

# def plot_season_data(input_path_waterflux, input_path_precip, sheet_name, start_date):

#     """Manual effort but rewarded by less complex code: provide a matching set of waterflux and precip data.
#     Specify which sheet and startdate, the sheet name are the ones from the data sheet (originate from factors to run),
#          and the start_date in factors to run matching with sheet_name also called case study (yes is confusion, inaccuracy of proper data logging at the start) """
#     # Load the Excel file, both need the same sheet names. which should be by default if matching sources
#     xls_waterflux = pd.ExcelFile(input_path_waterflux)
#     xls_precip = pd.ExcelFile(input_path_precip)


#     # Read the sheet into a DataFrame
#     df_waterflux = pd.read_excel(input_path_waterflux, sheet_name=sheet_name)
#     df_precip = pd.read_excel(input_path_precip, sheet_name=sheet_name)

#     # Calculate the date for each row based on the season's start date and dap. Both excel files should have the same number of rows if both are updated correctly
#     Dates = pd.to_datetime(start_date) + pd.to_timedelta(df_waterflux['time_step_counter'], unit='D')

#     # Extract the columns IrrDay from waterflux and precip_mm from precip
#     irrigation_data = df_waterflux['IrrDay']
#     precipitation_data = df_precip['precip_mm']

#     X_axis = np.arange(len(Dates))
#     fig, ax1 = plt.subplots(figsize=(10, 6))
#     # Plot
#     ax1.bar(X_axis - 0.2, df_waterflux['IrrDay'], 0.4, label='Irrigation', color='blue')
#     # Plot rain
#     ax1.bar(X_axis + 0.2, df_precip['precip_mm'], 0.4, label='Precipitation', color='orange')
#     # Add x-axis labels with rotation
#     plt.xticks(X_axis, Dates, rotation=90)
#     # Create a single plot with x-as the dates and Y-as the irrigation amount and precipitation amount in mm.
#     ax1.legend(['Irrigation amount (mm)', 'Precipitation amount (mm)'], loc='upper left')
#     plt.title('Crop Yield Comparison with Mean Bias Error (MBE) and Standard Deviation')
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.show()


# #     plt.figure(figsize=(20, 6))  # Adjust figure size as needed

# #     plt.plot(Dates, irrigation_data, label='Irrigation')
# #     plt.plot(Dates, precipitation_data, label='Precipitation')

# #     plt.xlabel('Date')
# #     plt.ylabel('mm')
# #     plt.title(f'Precipitation vs Irrigation for {sheet_name}')
# #     plt.legend()

# #     # Show or save the plot as needed
# #     plt.show()


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_season_data(input_path_waterflux, input_path_precip, sheet_name, start_date):
    # Load the Excel file, both need the same sheet names, which should be by default if matching sources
    xls_waterflux = pd.ExcelFile(input_path_waterflux)
    xls_precip = pd.ExcelFile(input_path_precip)

    # Read the sheet into a DataFrame
    df_waterflux = pd.read_excel(input_path_waterflux, sheet_name=sheet_name)
    df_precip = pd.read_excel(input_path_precip, sheet_name=sheet_name)

    # Calculate the date for each row based on the season's start date and dap.
    Dates = pd.to_datetime(start_date) + pd.to_timedelta(
        df_waterflux["time_step_counter"], unit="D"
    )

    # Set the datetime index to the calculated Dates
    df_waterflux.index = Dates
    df_precip.index = Dates

    # Resample the data to weekly frequency
    weekly_waterflux = df_waterflux[["IrrDay"]].resample("W", closed="right").sum()
    weekly_precip = df_precip[["precip_mm"]].resample("W", closed="right").sum()
    print(len(weekly_precip))

    X_axis = np.arange(len(weekly_waterflux))
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot irrigation and precipitation data
    ax1.bar(
        X_axis - 0.2, weekly_waterflux["IrrDay"], 0.4, label="Irrigation", color="blue"
    )
    ax1.bar(
        X_axis + 0.2,
        weekly_precip["precip_mm"],
        0.4,
        label="Precipitation",
        color="orange",
    )

    # Set x-axis labels as the calculated weekly dates
    plt.xticks(X_axis, weekly_waterflux.index.strftime("%Y-%m-%d"), rotation=45)

    # Create a single plot with x-axis as the dates and Y-axis as the irrigation and precipitation amount in mm.
    ax1.legend(
        ["Irrigation amount (mm)", "Precipitation amount (mm)"], loc="upper left"
    )
    plt.title("Crop Yield Comparison with Mean Bias Error (MBE) and Standard Deviation")
    plt.tight_layout()
    plt.show()


# Example usage:
# plot_season_data("path_to_waterflux.xlsx", "path_to_precip.xlsx", "Sheet1", "2023-01-01")
