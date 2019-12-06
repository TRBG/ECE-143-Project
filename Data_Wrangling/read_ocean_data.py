def read_ocean_data(fname,read_flag = 0):
    # -*- coding: utf-8 -*-
    """
    Created on Thu Nov  7 23:30:07 2019
    
    @author: albat
    """
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
            'Year':[], 'Month':[], 'Day':[],'Time':[], 'Bottom depth': [],
            'Depth':[], 'Temperatur':[], 'Salinity':[], 'Oxygen':[],
            'Phosphate':[],'Nitrate':[], 'pH':[] }
    
    set_of_measurements = {'Temperatur', 'Salinity', 'Oxygen', 'Phosphate', 'Nitrate', 'pH'}
    set_of_headers = {'CAST', 'Country', 'Latitude', 'Longitude', 'Year', 'Month', 'Day', 'Time', 'Bottom depth'}
    
    # The following code will retrieve the Cast reports and store them in the rows
    # list. Each list in the list rows (which is a list of lists) represent a line
    # in the reports.
    
    measurements_and_indices_list = []
    headers_and_indices_list = []
    
    cast_ind = 0
    total_num_of_measurements = 0
    
    rows =[]
    i = 0
    cast_important_indices = []
    
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
            elif 'VARIABLES' == row[0]:
                variables_strt_ind = i+3
                
                # Checking which variables are available in the cast
                avaialable_measurements = set_of_measurements.intersection(set(row))
                measurements_and_indices = [(x,row.index(x)) for x in avaialable_measurements]
                measurements_and_indices_list.append(measurements_and_indices)
                
                # Checking which of the cast headers is available in the cast
                header_rows = [x[0] for x in rows[cast_ind:variables_strt_ind-3]]
                #print(header_rows)
                avaialable_headers = set_of_headers.intersection(set(header_rows))
                headers_and_indices = [(x,header_rows.index(x)) for x in avaialable_headers]
                headers_and_indices_list.append(headers_and_indices)
                
                
                #print(i)
            elif 'END OF VARIABLES SECTION' == row[0]:
                #print(i)
                variables_end_ind = i-1
                num_of_measurements = variables_end_ind - variables_strt_ind + 1
                cast_important_indices.append((cast_ind,variables_strt_ind,num_of_measurements))
                
                total_num_of_measurements += num_of_measurements
            
            rows.append(row)
            i += 1
            
    
    # Setting up the dictionary with NA and nan values that later will be replaced with measurements
    # if they are available
    
    for key in Data:
        Data[key] = Data[key] + ['NA']*total_num_of_measurements
        
    for key in set_of_measurements:
        Data[key] = []
        Data[key] = Data[key] + ['nan']*total_num_of_measurements
      
        
    # Getting the measurements and putting them in the dictionary
    # 1111111111111111111111111111111111111
    
    measurement_ind = 0
    available_measurements_increment = 0
    for ind_set in cast_important_indices:
        
        measurements_and_indices = measurements_and_indices_list[available_measurements_increment]
        
        Data['Depth'][measurement_ind:measurement_ind+ind_set[2]] =\
            [measure[1] for measure in rows[ind_set[1]:ind_set[1]+ind_set[2]]]
        
        for x in measurements_and_indices:
            Data[x[0]][measurement_ind:measurement_ind+ind_set[2]] =\
            [measure[x[1]] for measure in rows[ind_set[1]:ind_set[1]+ind_set[2]]]
        
        measurement_ind += ind_set[2]
        available_measurements_increment+=1
        
    
    # Getting the cast information and putting them in the dictionary
    # 2222222222222222222222222222222222222222222222222222222222
    
    
    measurement_ind = 0
    available_headers_increment = 0
    
    for ind_set in cast_important_indices:
        
        headers_and_indices = headers_and_indices_list[available_headers_increment]
        
        for x in headers_and_indices:
            if x[0] == 'Country':
                Data['Country'][measurement_ind:measurement_ind+ind_set[2]] =\
                [rows[ind_set[0] + x[1]][4].capitalize()]*ind_set[2]
                
                Data['Country_Abr'][measurement_ind:measurement_ind+ind_set[2]] =\
                [rows[ind_set[0] + x[1]][2]]*ind_set[2]
                
            else:
                Data[x[0]][measurement_ind:measurement_ind+ind_set[2]] =\
                [rows[ind_set[0] + x[1]][2]]*ind_set[2]
        
        
        measurement_ind += ind_set[2]
        available_headers_increment +=1

    ##################################################
        
    end = time.time()
    print('The time it took to read ' + fname + ' is ' + str(round(end - start,2)) + ' seconds')
    
    start = time.time()
    df = pd.DataFrame(Data)
    wrangled_data_file_name = 'wrangled_data_of_' + fname
    df.to_csv(wrangled_data_file_name, index=False)
    end = time.time()
    print('The time it took to create a pandas datafram and write it to a datafram is ' + str(round(end - start,2)) + ' seconds')
