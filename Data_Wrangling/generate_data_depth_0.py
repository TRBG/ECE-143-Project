"""
This script  will read the cleaned data split by decade with day and night information
(stored in the files: cleaned_data_of_the_decade_with_day_night_info_comp.csv)
The data stored in these files have been generated in the script:
Day_night_measurement_step_2.py.

The purpose of this script is get the measurements at depth 0 (the surface of the ocean).
The code also removes all the casts that do not have a measurement of temperature
(all nan temperature values will be removed)

The title of the saved csv file will be:
all_data_depth_0_temp_nan_free_coordinates.csv.
"""

import pandas as pd
import time

#%% Reading the data and choosing a certain depth (for our analysis depth = 0)
decades = [(1950,1959), (1960,1969), (1970,1979), (1980,1989), \
           (1990,1999), (2000,2009), (2010,2018)]

for i in range(len(decades)):
    
    # reading the data and picking only the measurements recorded at depth = 0
    start = time.time()
    decades_data_fname = 'cleaned_data_of_the_' + str(decades[i][0]) + 's_with_day_night_info_comp.csv'
    df = pd.read_csv(decades_data_fname)
    
    df_dep_0_temp = df[df['Depth'] == 0]
    
    if i == 0:
        df_dep_0 = df_dep_0_temp.copy()
    
    else:
        df_dep_0 = pd.concat([df_dep_0, df_dep_0_temp]).copy()
    
    end = time.time()
    print('The time for the ' + str(decades[i][0]) + 's  =  ' +\
          str(round(end - start,2)) + ' seconds')

#%% Approximating the the latitudes and longitudes and removing nan temperature values
df_dep_0['Latitude_app'] = round(df_dep_0['Latitude'],0)
df_dep_0['Longitude_app'] = round(df_dep_0['Longitude'],0)

# creating a column that contains the approximated latitude and longitude (to nearest degree)
# for location based analysis 
df_dep_0_nan = df_dep_0[(df_dep_0.Temperatur.isna() == False)].copy()
df_dep_0_nan['coordinates'] = list(zip(df_dep_0_nan.Latitude_app, df_dep_0_nan.Longitude_app))

# Saving the dataframe to a csv file
df_dep_0_nan.to_csv('all_data_depth_0_temp_nan_free_coordinates.csv', index=False)



