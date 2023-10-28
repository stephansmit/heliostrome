import pandas as pd
import matplotlib.pyplot as plt

def plot_season_data(input_path_waterflux, input_path_precip, sheet_name, start_date): 
    """Manual effort but rewarded by less complex code: provide a matching set of waterflux and precip data. 
    Specify which sheet and startdate, the sheet name are the ones from the data sheet (originate from factors to run),
         and the start_date in factors to run matching with sheet_name also called case study (yes is confusion, inaccuracy of proper data logging at the start) """
    # Load the Excel file, both need the same sheet names. which should be by default if matching sources
    xls_waterflux = pd.ExcelFile(input_path_waterflux)
    xls_precip = pd.ExcelFile(input_path_precip)
    

    # Read the sheet into a DataFrame
    df_waterflux = pd.read_excel(input_path_waterflux, sheet_name=sheet_name)
    df_precip = pd.read_excel(input_path_precip, sheet_name=sheet_name)
    
    # Calculate the date for each row based on the season's start date and dap. Both excel files should have the same number of rows if both are updated correctly
    Dates = pd.to_datetime(start_date) + pd.to_timedelta(df_waterflux['time_step_counter'], unit='D')
    
    # Extract the columns IrrDay from waterflux and precip_mm from precip
    irrigation_data = df_waterflux['IrrDay']
    precipitation_data = df_precip['precip_mm']

    # Create a single plot with x-as the dates and Y-as the irrigation amount and precipitation amount in mm.
    plt.figure(figsize=(20, 6))  # Adjust figure size as needed

    plt.plot(Dates, irrigation_data, label='Irrigation')
    plt.plot(Dates, precipitation_data, label='Precipitation')

    plt.xlabel('Date')
    plt.ylabel('mm')
    plt.title(f'Precipitation vs Irrigation for {sheet_name}')
    plt.legend()

    # Show or save the plot as needed
    plt.show()
