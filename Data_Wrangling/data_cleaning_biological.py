# -*- coding: utf-8 -*-
"""
This script  will read the wrangled data (stored in the files: wrangled_normalized_biological_data_of_Data_i.csv,
where i is a number from 2 to 16). The data stored in these files have been wrangled
in the script: reading_wod_biological_data_script.py from the WOD cast reports.

After reading the wrangeld data and cleaning it, the script stores the data into a dataframe
cleaned_biological_data_i.csv where i goes from 2 to 16 as well.

THe code is very similar in structure to the one used for non-biological data

"""
def main():
    import pandas as pd
    import time
    
    for i in range(2,17):
        
        # reading the wrangled data
        start = time.time()
        fname =  'wrangled_normalized_biological_data_of_Data_' + str(i) + '.csv'
        df = pd.read_csv(fname)
        
        # cleaning the data
        cleaned_df = clean_dataframe(df)
        
        cleaned_data_fname = 'cleaned_biological_data_' + str(i) + '.csv'
        cleaned_df.to_csv(cleaned_data_fname, index=False)
        
        end = time.time()
        print('The time needed to read , clean, and save the data  is '\
              + str(round(end - start,2)) + ' seconds')


def clean_dataframe(df):
    
    # The names of the measurements (columns) of the dataframe that needs to be cleaned
    couls_to_clean = ['Total Wet Mass', 'Total Wet Mass Upper Depth', 'Total Wet Mass Lower Depth',\
                      'Displacemnt Vol', 'Displacemnt Vol Upper Depth', 'Displacemnt Vol Lower Depth',\
                      'Zooplankton Count', 'Zooplankton Count Upper Depth', 'Zooplankton Count Lower Depth']
    
    # removing the common issues found in the columns
    for column in couls_to_clean:
        df.loc[df[column] == '---0---', column] = 'nan'
        df.loc[df[column] == '**********', column] = 'nan'
        df[column] = df[column].astype(float)
        
    return df   

if __name__ == '__main__':
    main()


