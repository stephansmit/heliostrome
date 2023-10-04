import pandas as pd

def IRRschedule(A):
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
    Date = pd.to_datetime(Date, format='%d/%m/%Y')

    # Create the DataFrame
    schedule = pd.DataFrame({'Date': Date, 'Depth': Depth})

    return schedule
