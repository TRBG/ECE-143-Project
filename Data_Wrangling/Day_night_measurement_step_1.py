"""

This script  will read the cleaned data split by decade (stored in the files: 
cleaned_data_of_the_decade.csv, where decade is of the form 1950s, 1960s,..., 2010s). 
The data stored in these files have been generated in the script: splitting_by_decade.py.

The purpose of this script is to calculate the sunrise and sunset times for measurments
that have a sunrise and a sunset on the day of measurement.

For some latitudes where there are no sunrises and no sunsets (north and south latitudes)
during summer and winter and this is takled on the following script.

In this script the suntime pakage is used to calculate the sunrise and sunset times.
After that we will add an important column to our dataframe called 'day_night'
This column will indicate whether the measurement was taken during the day or
during the night. This column will be filled in the following script.

At the end the data is saved to a csv file that contain the sunrise and sunset times
of measurements (if available). The title of the csv files will be:
cleaned_data_of_the_decade_with_day_night_info.csv, where decade is of the form 
1950s, 1960s, ..., 2010s.

"""

# Importing the pakages needed 
import pandas as pd
import time
import numpy as np
from datetime import date
import datetime
from suntime import Sun, SunTimeException

# The list of decades used
decades = [(1950,1959), (1960,1969), (1970,1979), (1980,1989), \
           (1990,1999), (2000,2009), (2010,2018)]

a = 0

for i in range(len(decades)):
    
    # most of the calculations were done on numpy arrays to speed up the process
    # This allowed us to reduce the time of the operation of calculating sunrise
    # and sunset times from about 10 hours to few minutes
    start = time.time()
    decades_data_fname = 'cleaned_data_of_the_' + str(decades[i][0]) + 's.csv'
    df = pd.read_csv(decades_data_fname)
    
    # Defining some new columns that we will add to the dataframe
    df["day_night"] = ''
    df["noon_dawn"] = ''
    df['sunset_time_decimal'] = np.nan
    df['sunrise_time_decimal'] = np.nan
    
    # converting some of the dataframe columns to numpy arrays
    np_year = np.array(df['Year'])
    np_month = np.array(df['Month'])
    np_day = np.array(df['Month'])
    np_lat = np.array(df.Latitude)
    np_long = np.array(df.Longitude)
    np_sr = np.array([np.nan]*len(df))
    np_ss = np.array([np.nan]*len(df))
    np_cast = np.array(df.CAST)
    np_day_night = np.array([""]*len(df))
    
    # The following is an index list
    j_arr = []
    j_arr.append((np.nan,np.nan,np.nan))
    j_arr = j_arr*len(df)
    
    # finding the different casts (each cast can have more than one measurement)
    ind_array = np.where(np_cast[:-1] != np_cast[1:])[0]
    ind_array +=1   
    ind_array = np.concatenate(([0],ind_array), axis = 0)
    ind_array = np.concatenate((ind_array,[len(np_cast)-1]), axis = 0)
    
    # calculating the sunrise and sunset times for each cast (if possible)
    # If the lattitudes are in the far north or south during summer/winter
    # There are no sunrise or sunset as it will all be day or night
    # All the times are in UTC
    k = 0
    for j in range(len(ind_array)-1):
            
        d = date(np_year[ind_array[j]], np_month[ind_array[j]],np_day[ind_array[j]])
        sun = Sun(np_lat[ind_array[j]], np_long[ind_array[j]])
        
        try:
            sr = sun.get_sunrise_time(d)
            ss = sun.get_sunset_time(d)
            
        except:
            # Any operation here is needed for the try method
            k +=1
    
        else:
            # IF the sunrise can be calculated, then we use the suntime module
            # to compute the sunrise and sunset times for each cast
            sr = sun.get_sunrise_time(d)
            ss = sun.get_sunset_time(d)
            np_sr[ind_array[j]:ind_array[j+1]] = round(sr.hour + sr.minute/60,2)
            np_ss[ind_array[j]:ind_array[j+1]] = round(ss.hour + ss.minute/60,2)
            j_arr[j] = (ind_array[j],ind_array[j+1])
        
    
    # storing the numpy array to the dataframe
    df['sunrise_time_decimal'] = np_sr
    df['sunset_time_decimal'] = np_ss     
    
    # saving the dataframe to a csv file
    decades_data_fname = 'cleaned_data_of_the_' + str(decades[i][0]) + 's_with_day_night_info.csv'
    df.to_csv(decades_data_fname, index=False)
    
    end = time.time()
    print('The time for the ' + str(decades[i][0]) + 's  =  ' +\
          str(round(end - start,2)) + ' seconds')
