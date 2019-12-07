def read_biological_ocean_data(fname,read_flag = 0):
    """
     This function reades the WOD (biological surface) data stored in the file titled fname and then
    formulate the data into a tabular form and save it to a csv file titled:
    'wrangled_normalized_biological_data_of_' + fname + '.csv'.
    
    Some data files have NULL bytes and heance the read_flag will counter that
    (if equal to 1).
    
    The data files 11 and 13 are the ones that have null bytes for the dataset
    we used.
    
    Inputs:
    :parm fname: The name of the file that contains the WOD data
    :type fname: str
    
    :parm read_flag: A flag that specifies the method the data wil be read through
    :type fname: int
    """
    ##########################################################################
    # Input Validity Check
    assert isinstance(fname,str)
    assert isinstance(read_flag,int)
    assert (read_flag == 0 or read_flag == 1)
    
    ##########################################################################
    # Modules and pakages used
    import csv
    import time
    import pandas as pd
    
    
    start = time.time()
    # THe following is the dictionary that will contain the data.
    # It is created as a dictionary with lists as this is an optimum format to later create
    # a Pandas dataframe
    Data = {'CAST':[], 'Country':[], 'Country_Abr':[], 'Latitude':[], 'Longitude':[],
            'Year':[], 'Month':[], 'Day':[],'Time':[], 'Bottom depth': []}
    
    set_of_measurements = {'Total Wet Mass', 'Displacemnt Vol'}
    set_of_measurements_tuples = {('Total Wet Mass', '0.'), ('Displacemnt Vol', '0.')}
    
    set_of_total_measurements = {'Total Wet Mass',\
                                 'Total Wet Mass Unit', 'Total Wet Mass Upper Depth', 'Total Wet Mass Lower Depth',\
                                 'Displacemnt Vol',\
                                 'Displacemnt Vol Unit', 'Displacemnt Vol Upper Depth', 'Displacemnt Vol Lower Depth',\
                                 'Zooplankton Count',\
                                 'Zooplankton Count Unit', 'Zooplankton Count Upper Depth', 'Zooplankton Count Lower Depth'}
    
    set_of_headers = {'CAST', 'Country','Country_Abr' , 'Latitude', 'Longitude',\
                      'Year', 'Month', 'Day', 'Time', 'Bottom depth'}
    
    # The following code will retrieve the Cast reports and store them in the rows
    # list. Each list in the list rows (which is a list of lists) represent a line
    # in the reports.
    
    measurements_and_indices_list = []
    headers_and_indices_list = []
    
    cast_ind = 0
    
    rows =[]
    i = 0
    cast_important_indices = []
    
    start1 = time.time()
    with open(fname) as csvfile:
        if read_flag == 0:
            readCSV = csv.reader(csvfile, delimiter=',')
        else:
            readCSV = csv.reader(x.replace('\0', '') for x in csvfile)
        for row in readCSV:
            row = [x.strip() for x in row]
            
            if '#-----------' in row[0]:
                cast_ind = i
                #print(i)
            elif 'BIOLOGY' == row[0]:
                variables_strt_ind = i+1
                
                #print(i)
            elif 'END OF BIOLOGY SECTION' == row[0]:
                #print(i)
                variables_end_ind = i-1                
                
                # Checking which biological variables/measurements are available in the cast
                measurements_rows = [(x[3],x[1]) for x in rows[variables_strt_ind:variables_end_ind+1]]
                avaialable_measurements = set_of_measurements_tuples.intersection(set(measurements_rows))
                measurements_and_indices = [(x[0],measurements_rows.index(x)) for x in avaialable_measurements]
                
                taxon_rows = [(x[12],x[1]) for x in rows[variables_strt_ind:variables_end_ind+1]]
                for taxon_row in taxon_rows:
                    if ('ZOOPLANKTON','0.') in taxon_row:
                        zooplankton_count_location = ('Zooplankton Count',taxon_rows.index(taxon_row))
                        measurements_and_indices.append(zooplankton_count_location)
                
                
                    
                if len(measurements_and_indices) > 0:
                    measurements_and_indices_list.append(measurements_and_indices)
                
                    # Checking which of the cast headers is available in the cast
                    header_rows = [x[0] for x in rows[cast_ind:variables_strt_ind-3]]
                    #print(header_rows)
                    avaialable_headers = set_of_headers.intersection(set(header_rows))
                    headers_and_indices = [(x,header_rows.index(x)) for x in avaialable_headers]
                    headers_and_indices_list.append(headers_and_indices)
                
                
                    num_of_measurements = len(measurements_and_indices)
                    cast_important_indices.append((cast_ind,variables_strt_ind,num_of_measurements))
            
            rows.append(row)
            i += 1
            
    end1 = time.time()
    print('The time it took to read ' + fname + ' is ' + str(round(end1 - start1,2)) + ' seconds')
    # Setting up the dictionary with NA and nan values that later will be replaced with measurements
    # if they are available
    

    for key in set_of_headers:
        Data[key] = Data[key] + ['NA']*len(cast_important_indices)
        
    for key in set_of_total_measurements:
        Data[key] = []
        Data[key] = Data[key] + ['nan']*len(cast_important_indices)
        
        
    # Getting the measurements and putting them in the dictionary
    
    available_measurements_increment = 0
    
    for ind_set in cast_important_indices:
        
        measurements_and_indices = measurements_and_indices_list[available_measurements_increment]
        
        for x in measurements_and_indices:
            
                Data[x[0]][available_measurements_increment] =\
                rows[ind_set[1] + x[1]][7]
                
                unit_key = x[0] + ' Unit'
                Data[unit_key][available_measurements_increment] =\
                rows[ind_set[1] + x[1]][9]
                
                upper_depth_key = x[0] + ' Upper Depth'
                lower_depth_key = x[0] + ' Lower Depth'
                
                Data[upper_depth_key][available_measurements_increment] =\
                rows[ind_set[1] + x[1]][1]
                Data[lower_depth_key][available_measurements_increment] =\
                rows[ind_set[1] + x[1]][2]       

        available_measurements_increment+=1
        
    
    # Getting the cast information and putting them in the dictionary
    
    available_headers_increment = 0
    
    for ind_set in cast_important_indices:
        
        headers_and_indices = headers_and_indices_list[available_headers_increment]
        
        for x in headers_and_indices:
            if x[0] == 'Country':
                Data['Country'][available_headers_increment] =\
                rows[ind_set[0] + x[1]][4].capitalize()
                
                Data['Country_Abr'][available_headers_increment] =\
                rows[ind_set[0] + x[1]][2]
                
            else:
                Data[x[0]][available_headers_increment] =\
                rows[ind_set[0] + x[1]][2]
        
        
        available_headers_increment +=1

    ##################################################
        
    end = time.time()
    print('The time it took to read ' + fname + ' and create the dictionary is '\
          + str(round(end - start,2)) + ' seconds')
    
    start = time.time()
    
    df = pd.DataFrame(Data)
    wrangled_data_file_name = 'wrangled_normalized_biological_data_of_' + fname
    df.to_csv(wrangled_data_file_name, index=False)
    
    end = time.time()
    print('The time it took to create a pandas datafram and write it to a datafram is '\
          + str(round(end - start,2)) + ' seconds')
