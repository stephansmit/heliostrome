import pandas as pd

#A is respective field
#B is amount of simulation years. 1 is default. anything else will create an extended list with added years and depths for more simulations
def IRRschedule(A, B=1):
    IrrigationType = ['C1', 'C1', 'C1', 'C2', 'C2', 'C2', 'C2', 'C2', 'C2', 'C3', 'C3', 'C3', 'C3', 'V1', 'V1', 'V1', 'V2', 'V2', 'V2', 'V3', 'V3', 'V3', 'V4', 'V4', 'V4', 'V5', 'V5', 'V5', 'V6', 'V6', 'V6']

    if A == 0:
        Date = ['28/1/2006', '22/2/2006', '10/4/2006']
        Depth = [30] * 3
    elif A == 1:
        Date = ['1/2/2005', '21/2/2005', '14/3/2005', '24/3/2005', '7/4/2005', '24/4/2005']
        Depth = [30] * 6
    elif A == 2:
        Date = ['4/2/2005', '20/3/2005', '13/4/2005', '21/4/2005']
        Depth = [30] * 4
    elif A == 3:
        Date = ['20/1/2006', '23/2/2006', '1/4/2006']
        Depth = [60] * 3
    elif A == 4:
        Date = ['16/1/2006', '17/2/2006', '28/3/2006']
        Depth = [60] * 3
    elif A == 5:
        Date = ['20/1/2006', '15/2/2006', '17/3/2006']
        Depth = [60] * 3
    elif A == 6:
        Date = ['18/1/2006', '24/2/2006', '21/4/2006']
        Depth = [60] * 3
    elif A == 7:
        Date = ['16/1/2006', '16/2/2006', '26/3/2006']
        Depth = [60] * 3
    elif A == 8:
        Date = ['26/1/2006', '21/2/2006', '27/3/2006']
        Depth = [60] * 3
    else:
        return None  # Handle unknown A values

    # Convert Date strings to datetime objects
    base_dates = pd.to_datetime(Date, format='%d/%m/%Y')

    # Initialize lists to store extended Date and Depth
    extended_dates = []
    extended_depth = []

    # Create the DataFrame for the base year
    schedule = pd.DataFrame({'Date': base_dates, 'Depth': Depth})

    # Extend the DataFrame for B years with shifted dates and repeated depths
    for _ in range(B - 1):
        base_dates = [d + pd.DateOffset(years=1) for d in base_dates]
        extended_dates.extend(base_dates)
        extended_depth.extend(Depth)

    # Create a DataFrame for the extended data
    extended_schedule = pd.DataFrame({'Date': extended_dates, 'Depth': extended_depth})

    # Concatenate the base schedule with the extended schedule
    schedule = pd.concat([schedule, extended_schedule], ignore_index=True)

    #schedule = schedule.append(pd.DataFrame({'Date': extended_dates, 'Depth': extended_depth}), ignore_index=True)

    return schedule

