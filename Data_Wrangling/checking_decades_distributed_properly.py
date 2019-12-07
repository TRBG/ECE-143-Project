"""
This code checks that we splitted the data by decade properly in the script
splitting_by_decde.py.

"""

def main():
    # The modeules needed
    import pandas as pd
    import time
    
    # The decades edges lst
    decades = [(1950,1959), (1960,1969), (1970,1979), (1980,1989), \
               (1990,1999), (2000,2009), (2010,2018)]
    
    # We will iterate and make sure that we have the data from the specific
    # decade only and not other decades
    start = time.time()
    for i in range(len(decades)):
        start = time.time()
        
        # reading the datafile and storing it to dataframe
        decades_data_fname = 'cleaned_data_of_the_' + str(decades[i][0]) + 's.csv'
        df = pd.read_csv(decades_data_fname)
        
        # checkig if there are other decades in the dataframe
        df = df[df.Year < decades[i][0]]
        df = df[df.Year > decades[i][1]]
        
        # if there is other decades, we print a message that there is something wrong
        if df.empty == False:
            print('Something went Wrong :(')
        end = time.time()
        
        print('The time for the ' + str(decades[i][0]) + 's  =  ' +\
              str(round(end - start,2)) + ' seconds')

if __name__ == '__main__':
    main()