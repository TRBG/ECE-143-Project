# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 02:33:38 2019

@author: albat
"""

def main():
    import pandas as pd
    import time
    
    decades = [(1950,1959), (1960,1969), (1970,1979), (1980,1989), \
               (1990,1999), (2000,2009), (2010,2018)]
    
    start = time.time()
    for i in range(len(decades)):
        start = time.time()
        
        decades_data_fname = 'cleaned_data_of_the' + str(decades[i][0]) + 's.csv'
        df = pd.read_csv(decades_data_fname)
        
        df = df[df.Year < decades[i][0]]
        df = df[df.Year > decades[i][1]]
        
        
        if df.empty == False:
            print('Something went Wrong :(')
        end = time.time()
        
        print('The time for the ' + str(decades[i][0]) + 's  =  ' +\
              str(round(end - start,2)) + ' seconds')

if __name__ == '__main__':
    main()