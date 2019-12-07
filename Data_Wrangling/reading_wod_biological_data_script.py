
"""
In this script we wil load the World Oceanic Data (WOD) that have been 
requested from National Oceanic and Atmospheric Administration (NOAA).

The WOD has been requested from NOAA through their WODselect service available
at (https://www.nodc.noaa.gov/OC5/SELECT/dbsearch/dbsearch.html)

Through this service an inquiry was made to request non-biological and biological
Oceanic Station Data (OSD) from the 1900 to 2018.

The OSD is stored as CAST reports in csv files. These csv files are not regular
csv tabular data, but rather a set of reports. Openning one fo these files in
Excel or a text editor will highlight twhat we mean by this.

The WOD data for the years 1950 to 2018 are in the datafiles Data_2.csv to 
Data_16.csv. These CSV files are not tabular data. They are OSD casts saved in
csv file

This code will read the biological data

"""

from read_biological_ocean_data import read_biological_ocean_data

#%% Reading the data

# The files are named Data_2 to Data_16 (They conatin the data from 1950 to 2018)
file_indices = list(range(2,17))

for i in file_indices:
    
    if i in [11,13]:
        # Some of the files contain NULL bytes and hence a special method is 
        # needed to read them. This method is utilized based on the read_flag
        # value. The file numbers are int the list of the if conditional.
        read_flag = 1;
    else:
        read_flag = 0;
        
    fname = 'Data_' + str(i) + '.csv'
    print(fname)
    # The following function is the function used to read the data and save it
    # to tabular csv file called wrangled_data_of_Data_i.csv
    read_biological_ocean_data(fname, read_flag)
    
