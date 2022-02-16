"""Datetime module containing datetime functions set up for a 360 day year
e.g. to convert from datenum to datetime and visa versa """
import numpy as np


def createyear360(n_year, start_year = 2000):
    """Creates a list of datetimes in the form yyyy-mm-dd for a 360 day year
    Args: n_year = number of years
          start_year = starting year, default = 2000"""
    ys = np.arange(start_year, start_year + n_year) 
    year360 = np.zeros((n_year*360, 3), dtype=int)
    for i in range(n_year):
        years = np.repeat(ys[i], 360) 
        months = np.repeat(np.arange(1,13), 30)  
        days   = np.tile(np.arange(1, 31), 12)
        year360[i*360:(i+1)*360,:] = np.stack((years, months, days), axis=-1) 
    return(year360)


def datenum360(datetimes):
    """Calculates datetimes as datenum when using 360 day years
    datetimes is a np array of datetimes of form (year, mon, day)
    Shape is [n_dates, 3], e.g. array([[2000, 1, 1], [2000, 1, 2]]) """
    start_date = [0, 1, 1]
    years = datetimes[:,0]
    months = datetimes[:,1]
    days = datetimes[:,2]
    days_since = years*360 + months*30 + days   # days since 0000-01-01
    return(days_since)


def datetime360(datenum):
    """Calculates datetime from datenums when using 360 day years"""
    # First check for nans, note that these result in datetime [-3, 2, 20]
    datenum[np.isnan(datenum)] = -1e3

    start_date = [0, 1, 1]
    # Years are divided by 360 and floor-ed
    years = np.floor(datenum/360.0)

    # Months we take the remainder and do the same with 30 days
    datenum1 = np.mod(datenum, 360);
    months = np.floor((datenum1-1)/30.0);    
    # Month = 0 should be Month = 12 of previous year
    years[months==0] = years[months==0] - 1;
    months[months==0] = 12;
    
    # Days we take the remainder again
    days = np.mod(datenum1, 30);
    #print(days)
    # Day = 0  should be Day = 30 of previous month
    days[(days==0)] = 30
    
    # Check all are ints
    years = np.ndarray.astype(years, int) 
    months = np.ndarray.astype(months, int) 
    days = np.ndarray.astype(days, int) 
    datetime = np.stack((years, months, days), axis=-1) 
    
    return(datetime)
