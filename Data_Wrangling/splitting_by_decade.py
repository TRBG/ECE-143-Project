# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 00:13:24 2019

@author: albat
"""
def main():
    import pandas as pd
    import time
    
    decades = [(1950,1959), (1960,1969), (1970,1979), (1980,1989), \
               (1990,1999), (2000,2009), (2010,2018)]
    
    dataframe_ind = 2
    
    for i in range(len(decades)):
        
        start = time.time()
        fname =  'cleaned_data_' + str(dataframe_ind) + '.csv'
        df = pd.read_csv(fname)
        
        df = df[df.Year >= decades[i][0]]
        df = df[df.Year <= decades[i][1]]
        
        
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
                
        
        decades_data_fname = 'cleaned_data_of_the' + str(decades[i][0]) + 's.csv'
        df.to_csv(decades_data_fname, index=False)
        
        end = time.time()
        print('The time for the ' + str(decades[i][0]) + 's  =  ' +\
              str(round(end - start,2)) + ' seconds')

            

if __name__ == '__main__':
    main()


