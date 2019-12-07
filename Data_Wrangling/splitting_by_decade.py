# -*- coding: utf-8 -*-
"""

This script  will read the cleaned data (stored in the files: cleaned_data_i.csv,
where i is a number from 2 to 16). The data stored in these files have been cleaned
in the script: data_cleaning.py.

After reading the cleaned data and splitting it by decade, the script stores 
the data into a dataframe and save it to a csv file titled: 
cleaned_data_of_the_decade.csv, where decade is of the form 1950s, 1950s, ...
2010s.

The reason we are splitting the data by decade is the data is huge and we decided
to divide it through a reasonable time based divider.

"""
def main():
    import pandas as pd
    import time
    
    # The edges of the decades
    decades = [(1950,1959), (1960,1969), (1970,1979), (1980,1989), \
               (1990,1999), (2000,2009), (2010,2018)]
    
    # The file indix as our files are ordered (check the data_cleaning.py) from 2
    # to 16
    dataframe_ind = 2
    
    # We will go over each decade and store all the data in that decade to a 
    # csv file
    for i in range(len(decades)):
        
        # reading the cleaned data file and saving it to a datframe
        start = time.time()
        fname =  'cleaned_data_' + str(dataframe_ind) + '.csv'
        df = pd.read_csv(fname)
        
        # getting all the data in this file that are in the specified decade
        df = df[df.Year >= decades[i][0]]
        df = df[df.Year <= decades[i][1]]
        
        # The following part will check if there are data in the specified decade
        # in other files and fetch them then store them in the dataframe
        if df[df.Year > decades[i][1]].empty == True:
            dataframe_ind +=1
            
            while dataframe_ind <= 16:
                
                fname =  'cleaned_data_' + str(dataframe_ind) + '.csv'
                df1 = pd.read_csv(fname)
                df = pd.concat([df,df1[df1.Year <= decades[i][1]]])
                
                if df1[df1.Year > decades[i][1]].empty == True:
                    dataframe_ind +=1
                else:
                    break
                
        # storing all the data of the specified decade into a csv file.
        decades_data_fname = 'cleaned_data_of_the_' + str(decades[i][0]) + 's.csv'
        df.to_csv(decades_data_fname, index=False)
        
        end = time.time()
        print('The time for the ' + str(decades[i][0]) + 's  =  ' +\
              str(round(end - start,2)) + ' seconds')

            

if __name__ == '__main__':
    main()


