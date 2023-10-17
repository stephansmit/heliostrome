import pandas as pd
import matplotlib.pyplot as plt

def plot_season_data(input_path, start_dates): 
    """input the file of cleaned waterflux with the full row of 
    the excel data for start date, it needs a list of startdates as long as the amount of sheets in waterflux (should always match up if files are related)"""
    # Load the Excel file
    xls = pd.ExcelFile(input_path)
    
    # Initialize a list to store data for each season
    season_data = []

    for sheet_name, start_date in zip(xls.sheet_names, start_dates):
        # Read the sheet into a DataFrame
        df = pd.read_excel(input_path, sheet_name=sheet_name)
        
        # Calculate the date for each row based on the season's start date and dap
        df['Date'] = pd.to_datetime(start_date) + pd.to_timedelta(df['time_step_counter'], unit='D')
        
        # Group data by the 'season_counter' column
        grouped = df.groupby('season_counter')
        
        # Iterate through seasons and store the data
        for season, group in grouped:
            season_data.append((group['Date'], group['IrrDay'], f'Season {season}'))

        # Create a single plot with overlapping lines
        plt.figure(figsize=(20, 6))  # Adjust figure size as needed
        
        for date, irrday, label in season_data:
            plt.plot(date, irrday, label=label)
            
        plt.xlabel('Date')
        plt.ylabel('IrrDay')
        plt.title(f'IrrDay Over Days of Season for {sheet_name}')
        plt.legend()
    
        # Show or save the plot as needed
        plt.show()