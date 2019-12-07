"""
This script  will read the wrangled data (stored in the files: wrangled_data_of_Data_i.csv,
where i is a number from 2 to 16). The data stored in these files have been wrangled
in the script: reading_wod_data_script.py from the WOD cast reports.

After reading the wrangeld data and cleaning it, the script stores the data into a dataframe
cleaned_data_of_Data_i.csv where i goes from 2 to 16 as well.

"""
def main():
    import pandas as pd
    import time
    
    # i is the number (index of the file that will be read and cleaned)
    for i in range(2,17):
        
        start = time.time()
        fname =  'wrangled_data_of_Data_' + str(i) + '.csv'
        
        # a warning message that there are mixed type columns will be displayed.
        # This is OK and can be ignored. One of the targets of cleaning the data
        # is to overcome this problem.
        df = pd.read_csv(fname)
        
        # The function clean_dataframe is used to remove several issues with
        # non biological measurements in the data.
        cleaned_df = clean_dataframe(df)
        
        # saving the dataframe to a csv file titled cleaned_data_i.casv, where
        # i goes from 2 to 16
        cleaned_data_fname = 'cleaned_data_' + str(i) + '.csv'
        cleaned_df.to_csv(cleaned_data_fname, index=False)
        
        end = time.time()
        print('The time needed to read , clean, and save data No.' + str(i) + ' out of 16 is '\
              + str(round(end - start,2)) + ' seconds')


def clean_dataframe(df):
    
    # The following are the non-biological measurements that will be cleaned
    couls_to_clean = ['Temperatur', 'Salinity', 'Oxygen', 'Phosphate',\
                      'Nitrate', 'pH']
    
    # The issues that need fixing in the data. WE will replace them with nan
    # Then in a following script we will remove nan values based on the analysis
    for column in couls_to_clean:
        df.loc[df[column] == '---0---', column] = 'nan'
        df.loc[df[column] == '**********', column] = 'nan'
        df[column] = df[column].astype(float)
        
    return df   

if __name__ == '__main__':
    main()


