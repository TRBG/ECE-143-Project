"""
This script  will read the cleaned data split by decade with sunrise and sunset
meaeured (stored in the files: cleaned_data_of_the_decade_with_day_night_info.csv)
The data stored in these files have been generated in the script:
Day_night_measurement_step_1.py.

The purpose of this script is assign wether the measurements were taken during
the day or the night into the column of our dataframe called 'day_night' which was created
in the previous script (Day_night_measurement_step_1.py).

At the end the data is saved to a csv file that contain the day and night assignments
of measurements (if available). The title of the csv files will be:
cleaned_data_of_the_decade_with_day_night_info_comp.csv, where decade is of the form 
1950s, 1960s, ..., 2010s.

"""

# The modules used
import pandas as pd
import time
import numpy as np
from datetime import date
import math


# The list of decades edges
decades = [(1950,1959), (1960,1969), (1970,1979), (1980,1989), \
           (1990,1999), (2000,2009), (2010,2018)]

a = 0

for i in range(len(decades)):
    
    # The work is done again in numpy to speed up the calculations
    # The columns are assigned to numpy arrays
    start = time.time()
    decades_data_fname = 'cleaned_data_of_the_' + str(decades[i][0]) + 's_with_day_night_info.csv'
    df = pd.read_csv(decades_data_fname)
    df["day_night"] = ''
    df["deep_day_night"] = ''
    np_year = np.array(df['Year'])
    np_month = np.array(df['Month'])
    np_day = np.array(df['Day'])
    np_time = np.array(df['Time'])
    np_lat = np.array(df.Latitude)
    np_long = np.array(df.Longitude)
    np_sr = df['sunrise_time_decimal']
    np_ss = df['sunset_time_decimal']
    np_day_length = np.array([np.nan]*len(df))
    np_cast = np.array(df.CAST)
    np_day_night = np.array(["NA"]*len(df))
    np_deep_day_night = np.array(["NA"]*len(df))
    np_time = np.array(df.Time)
    
    #%% The following code will determine the day or night if the sunset and sunrise times were calculated
    
    # When sunset is larger in value than sunrise (24 hour system is used and times in UTC)
    day_time = np.where(((np_ss > np_sr) &  ((np_time < np_ss) & (np_time > np_sr))))[0]
    np_day_night[day_time] = 'd'
    del day_time
    
    deep_day_time = np.where((np_day_night == 'd') & (np_ss > np_sr) & ((np_time - np_sr) > 2) & ((np_time - np_ss) < -2))[0]
    np_deep_day_night[deep_day_time] = 'dd'
    del deep_day_time
    
    night_time = np.where(((np_ss > np_sr) &  ((np_time > np_ss) | (np_time < np_sr))))[0]
    np_day_night[night_time] = 'n'
    del night_time
    
    deep_night_time = np.where((np_day_night == 'n') & (np_ss > np_sr) & (((np_time - np_ss) > 2) | ((np_time + 24 - np_ss) < 2)) & \
                               (((np_time - np_sr) < -2) | ((np_time - (np_sr +24)) <-2)))[0]                                    
    np_deep_day_night[deep_night_time] = 'dn'
    del deep_night_time
    
    
    # When sunset is smaller in value than sunrise (24 hour system is used and times in UTC)
    day_time = np.where(((np_ss < np_sr) &  ((np_time < np_ss) | (np_time > np_sr))))[0]
    np_day_night[day_time] = 'd'
    del day_time
    
    deep_day_time = np.where((np_day_night == 'd') & (np_ss < np_sr) & (((np_time - np_sr) > 2) | ((np_time + 24 - np_sr) < 2)) & \
                               (((np_time - np_ss) < -2) | ((np_time - (np_ss +24)) <-2)))[0] 
    np_deep_day_night[deep_day_time] = 'dd'
    del deep_day_time
    
    night_time = np.where(((np_ss < np_sr) &  ((np_time > np_ss) & (np_time < np_sr))))[0]
    np_day_night[night_time] = 'n'
    del night_time
    
    deep_night_time = np.where((np_day_night == 'n') & (np_ss < np_sr) & ((np_time - np_sr) < -2) & ((np_time - np_ss) > 2))[0]
    np_deep_day_night[deep_night_time] = 'dn'
    del deep_night_time
    
    #%% The following code will determine the day or night if the sunset and sunrise times were not calculted
    
    # Finding the indices of the start of each cast
    ind_array = np.where(np_cast[:-1] != np_cast[1:])[0]  # This will get the indices where there is a change
    ind_array = np.concatenate(([0],ind_array), axis = 0)  # This will add the indix 0
    ind_array = np.concatenate((ind_array,[len(np_cast)-1]), axis = 0)
    # putting the index of the start and end of each cast in tuples
    ind_tuples = np.array([(ind_array[i]+1,ind_array[i+1]) for i in range(len(ind_array)-1)])
    del ind_array
    
    # Finding where the sunrise is nan and other important info is not nan
    ind_array_sr = np.where(np.isnan(np_sr))[0]
    ind_array_import_info = np.where((np.isnan(np_lat) == False) & (np.isnan(np_year) == False) &\
                                     (np.isnan(np_month) == False) & (np.isnan(np_day) == False))[0]
    
    ind_array_total = np.intersect1d(ind_array_import_info, ind_array_sr)
    
    # The following is the for the northern hemisphere
    ind_north = np.where(np_lat > 0)[0]   # Will get teh indices where the latitude is higher than 0
    ind_array_total_1 = np.intersect1d(ind_array_total, ind_north)    # Intersection with important info
    ind_tuples_2 = ind_tuples[np.isin(ind_tuples[:,0],ind_array_total_1)]    # The indices of the cast that are north and had no sunrise
    
    del ind_north
    del ind_array_total_1
    del ind_array_import_info
    del ind_array_sr
    
    for k in ind_tuples_2:
        
        # l = latitude
        # The following is maximum latitude where we will not get a full day or a full night
        # We are using this to make sure the trignometric functions used to calculate the day length
        # doesn't crash (by returning infinity) if the day length is large then it is an all day
        # if it is small then it is all night because we are calculating this for only the dates and locations
        # that we were not able to calculate the sunrise and senset for (There were none --> all night or all day)
        l = 65
        try:
            d = date(np_year[k[0]],np_month[k[0]],np_day[k[0]])
        except: 
            kkkkk = 1
        else:
            j = j = d.timetuple().tm_yday
            
            # The following is the mathematical calculation to calculate teh length of the day (approximate)
            p = np.arcsin(0.39795*np.cos(0.2163108 + 2*np.arctan(0.9671396*np.tan(.00860*(j-186)))))
            D = 24 - (24/math.pi)*np.arccos((np.sin(0.8333*math.pi/180)+np.sin(l*math.pi/180)*np.sin(p))/(np.cos(l*math.pi/180)*np.cos(p)))
    
            np_day_length[k[0]:k[1]+1] = D
    
    del ind_tuples_2

  # The following is the for the southern hemisphere
    ind_south = np.where(np_lat  < 0)[0]   # Will get teh indices where the latitude is higher than 0
    ind_array_total_2 = np.intersect1d(ind_array_total, ind_south)    # Intersection with important info
    ind_tuples_3 = ind_tuples[np.isin(ind_tuples[:,0],ind_array_total_2)]    # The indices of the cast that are north and had no sunrise
    del ind_tuples
    del ind_array_total
    del ind_array_total_2
    del ind_south
    
    for k in ind_tuples_3:
        
        # l = latitude
        # The following is maximum latitude where we will not get a full day or a full night
        # We are using this to make sure the trignometric functions used to calculate the day length
        # doesn't crash (by returning infinity) if the day length is large then it is an all day
        # if it is small then it is all night because we are calculating this for only the dates and locations
        # that we were not able to calculate the sunrise and senset for (There were none --> all night or all day)
        l = -65
        try:
            d = date(np_year[k[0]],np_month[k[0]],np_day[k[0]])
        except:
            kkkkk = 1
        else:
            j = j = d.timetuple().tm_yday
            
            # The following is the mathematical calculation to calculate teh length of the day (approximate)
            p = np.arcsin(0.39795*np.cos(0.2163108 + 2*np.arctan(0.9671396*np.tan(.00860*(j-186)))))
            D = 24 - (24/math.pi)*np.arccos((np.sin(0.8333*math.pi/180)+np.sin(l*math.pi/180)*np.sin(p))/(np.cos(l*math.pi/180)*np.cos(p)))
    
            np_day_length[k[0]:k[1]+1] = D     
         
         
    print('ended the run') 
    
    del ind_tuples_3 
    
    # Assigning the night and day categories
    day_time = np.where(np_day_length > 18)[0]
    np_day_night[day_time] = 'd'
    
    night_time = np.where(np_day_length < 6)[0]
    np_day_night[night_time] = 'n'
    
    df["day_night"] = np_day_night
    df["deep_day_night"] = np_deep_day_night

 
    # Saving the dataframe
    decades_data_fname = 'cleaned_data_of_the_' + str(decades[i][0]) + 's_with_day_night_info_comp.csv'
    df.to_csv(decades_data_fname, index=False)
    
    end = time.time()
    print('The time for the ' + str(decades[i][0]) + 's  =  ' +\
          str(round(end - start,2)) + ' seconds')


