# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 00:13:24 2019

@author: albat
"""
def main():
    import pandas as pd
    import time
    
    for i in range(3,17):
        
        start = time.time()
        fname =  'wrangled_data_of_Data_' + str(i) + '.csv'
        df = pd.read_csv(fname)
        
        cleaned_df = clean_dataframe(df)
        
        cleaned_data_fname = 'cleaned_data_' + str(i) + '.csv'
        cleaned_df.to_csv(cleaned_data_fname, index=False)
        
        end = time.time()
        print('The time needed to read , clean, and save the data  is '\
              + str(round(end - start,2)) + ' seconds')


def clean_dataframe(df):
    
    couls_to_clean = ['Temperatur', 'Salinity', 'Oxygen', 'Phosphate',\
                      'Nitrate', 'pH']

    for column in couls_to_clean:
        df.loc[df[column] == '---0---', column] = 'nan'
        df.loc[df[column] == '**********', column] = 'nan'
        df[column] = df[column].astype(float)
        
    return df   

if __name__ == '__main__':
    main()


