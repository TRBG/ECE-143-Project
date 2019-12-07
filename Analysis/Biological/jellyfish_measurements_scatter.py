#%%
######################################
# Read ocean and jelly fish data     # 
######################################
def read_ocean_data(fname):
    '''This function read the ckeaned ocean data and extract
       only the surface ones
       fname: data name
    '''
    assert isinstance(fname, str)
    import pandas as pd

    dat = pd.read_csv(fname)
    dat = dat[dat['Depth'] == 0]

    return dat

import pandas as pd
import math 

dat = pd.read_csv('jelly_fish.csv')
dat = dat[(dat['year'] >=1950) & (dat['count_actual'] != 'nd')] 
ocean_dat_2010s = read_ocean_data('cleaned_data_of_the2010s.csv')
ocean_dat_2000s = read_ocean_data('cleaned_data_of_the2000s.csv')
ocean_dat_1990s = read_ocean_data('cleaned_data_of_the1990s.csv')
ocean_dat_1980s = read_ocean_data('cleaned_data_of_the1980s.csv')
ocean_dat_1970s = read_ocean_data('cleaned_data_of_the1970s.csv')
ocean_dat_1960s = read_ocean_data('cleaned_data_of_the1960s.csv')
ocean_dat_1950s = read_ocean_data('cleaned_data_of_the1950s.csv')

#%%
##############################################
# split the jellyfish data by decades        #
##############################################
a = []
b = []
c = []
jellyfish_2010s= set()
jellyfish_2000s= set()
jellyfish_1990s= set()
jellyfish_1980s= set()
jellyfish_1970s= set()
jellyfish_1960s= set()
jellyfish_1950s= set()

for i in dat[dat['count_actual']!='nd']['lat']:
    a.append(i)
for i in dat[dat['count_actual']!='nd']['lon']:
    b.append(i)
for i in dat[dat['count_actual']!='nd']['year']:
    c.append(i)
for i in range(len(a)):
    if c[i] >= 2000 and c[i] <= 2009:
        jellyfish_2000s.add((c[i], a[i], b[i]))
    elif c[i] >= 2010 and c[i] <= 2019:
        jellyfish_2010s.add((c[i], a[i], b[i]))
    elif c[i] >= 1990 and c[i] <= 1999:
        jellyfish_1990s.add((c[i], a[i], b[i]))
    elif c[i] >= 1980 and c[i] <= 1989:
        jellyfish_1980s.add((c[i], a[i], b[i]))
    elif c[i] >= 1970 and c[i] <= 1979:
        jellyfish_1970s.add((c[i], a[i], b[i]))
    elif c[i] >= 1960 and c[i] <= 1969:
        jellyfish_1960s.add((c[i], a[i], b[i]))
    elif c[i] >= 1950 and c[i] <= 1959:
        jellyfish_1950s.add((c[i], a[i], b[i]))   
    
#%%
####################################################################################
# This function returns the average count in the jellyfish data and the average of #
# different oceaninc measurement by the same latitude and longitude                #
####################################################################################
def ocean_jellyfish_conbine(jellyfish, ocean_dat, dat, measurement):
    '''This function returns the average count in the jellyfish data and the average
       of different oceaninc measurement by the same latitude and longitude 
       jellyfish: jellyfish data split by dacade
       ocean_data: ocean data
       dat: oringinal jellyfish data
       measurement: measurement name that interested in 
    '''
    import pandas as pd
    assert isinstance(jellyfish, set)
    assert isinstance(ocean_dat, pd.DataFrame)
    assert isinstance(dat, pd.DataFrame)
    assert isinstance(measurement, str)
    ave_count = []
    ave_temp = []

    for i in jellyfish:
        sum_count = 0
        sum_temp = 0
        count_count = 0
        count_temp = 0
        for j in dat[(dat['year'] == i[0]) & (dat['lat'] >= i[1]-0.5) & (dat['lat'] <= i[1] + 0.5)
                    & (dat['lon'] >= i[2] - 0.5)& (dat['lon'] <=  i[2] + 0.5)]['count_actual']:

            sum_count += int(j)
            count_count += 1
        ave_count.append(sum_count/count_count)

        aa =  ocean_dat[(ocean_dat['Year'] == i[0]) & (ocean_dat['Latitude'] >= i[1]-0.5) & (ocean_dat['Latitude'] <= i[1] + 0.5)
                    & (ocean_dat['Longitude'] >= i[2] - 0.5) & (ocean_dat['Longitude'] <=  i[2] + 0.5)][measurement]
        if len(aa) != 0:
            for j in aa:
                if not math.isnan(j):
                    sum_temp += j
                    count_temp += 1
            if count_temp != 0:
                ave_temp.append(sum_temp/count_temp)
            else:
                ave_temp.append(float('nan'))        
        else:
            ave_temp.append(float('nan'))

    return ave_count, ave_temp
#%%
#################################################################
# collect and conbine average temperature and average count for #
# different decades and do the plotting                         #
#################################################################

# collect ave_count and ave_temp
ave_count = []
ave_temp = []

a, b = ocean_jellyfish_conbine(jellyfish_2010s, ocean_dat_2010s, dat, 'Temperatur')
ave_count += a
ave_temp += b

a, b = ocean_jellyfish_conbine(jellyfish_2000s, ocean_dat_2000s, dat, 'Temperatur')
ave_count += a
ave_temp += b

a, b = ocean_jellyfish_conbine(jellyfish_1990s, ocean_dat_1990s, dat, 'Temperatur')
ave_count += a
ave_temp += b

a, b = ocean_jellyfish_conbine(jellyfish_1980s, ocean_dat_1980s, dat, 'Temperatur')
ave_count += a
ave_temp += b

a, b = ocean_jellyfish_conbine(jellyfish_1970s, ocean_dat_1970s, dat, 'Temperatur')
ave_count += a
ave_temp += b

a, b = ocean_jellyfish_conbine(jellyfish_1960s, ocean_dat_1960s, dat, 'Temperatur')
ave_count += a
ave_temp += b

a, b = ocean_jellyfish_conbine(jellyfish_1950s, ocean_dat_1950s, dat, 'Temperatur')
ave_count += a
ave_temp += b
# Remove the outlier 
ave_count_1 = []
ave_temp_1 = []
for i in range(len(ave_temp)):
    if ave_count[i] < 140000:
        ave_count_1.append(ave_count[i])
        ave_temp_1.append(ave_temp[i])
# scatter plot 
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
sns.set(style = 'darkgrid')
g = sns.jointplot(ave_temp_1, ave_count_1)
g = g.plot(sns.regplot, sns.distplot)
g.set_axis_labels('Temperature', 'Jelly Fish Average Count')
g.annotate(stats.pearsonr)
g.savefig('jellyfish_Temperature.png')


#%%
#################################################################
# collect and conbine average salinity and average count for    #
# different decades and do the plotting                         #
#################################################################

# collect ave_salinity and ave_count 
ave_count = []
ave_salinity = []

a, b = ocean_jellyfish_conbine(jellyfish_2010s, ocean_dat_2010s, dat, 'Salinity')
ave_count += a
ave_salinity += b

a, b = ocean_jellyfish_conbine(jellyfish_2000s, ocean_dat_2000s, dat, 'Salinity')
ave_count += a
ave_salinity += b

a, b = ocean_jellyfish_conbine(jellyfish_1990s, ocean_dat_1990s, dat, 'Salinity')
ave_count += a
ave_salinity += b

a, b = ocean_jellyfish_conbine(jellyfish_1980s, ocean_dat_1980s, dat, 'Salinity')
ave_count += a
ave_salinity += b

a, b = ocean_jellyfish_conbine(jellyfish_1970s, ocean_dat_1970s, dat, 'Salinity')
ave_count += a
ave_salinity += b

a, b = ocean_jellyfish_conbine(jellyfish_1960s, ocean_dat_1960s, dat, 'Salinity')
ave_count += a
ave_salinity += b

a, b = ocean_jellyfish_conbine(jellyfish_1950s, ocean_dat_1950s, dat, 'Salinity')
ave_count += a
ave_salinity += b
# Remove the outlier 
ave_count_1 = []
ave_salinity_1 = []
for i in range(len(ave_salinity)):
    if ave_count[i] < 140000:
        ave_count_1.append(ave_count[i])
        ave_salinity_1.append(ave_salinity[i])
# scatter plot 
sns.set(style = 'darkgrid')
g = sns.jointplot(ave_salinity_1, ave_count_1)
g = g.plot(sns.regplot, sns.distplot)
g.set_axis_labels('Salinity', 'Jelly Fish Average Count')
g.annotate(stats.pearsonr)
g.savefig('jellyfish_Salinity.png')

#%%
#################################################################
# collect and conbine average oxygen and average count for      #
# different decades and do the plotting                         #
#################################################################

# collect ave_oxygen and ave_count 
ave_count = []
ave_oxygen = []

a, b = ocean_jellyfish_conbine(jellyfish_2010s, ocean_dat_2010s, dat, 'Oxygen')
ave_count += a
ave_oxygen += b

a, b = ocean_jellyfish_conbine(jellyfish_2000s, ocean_dat_2000s, dat, 'Oxygen')
ave_count += a
ave_oxygen += b

a, b = ocean_jellyfish_conbine(jellyfish_1990s, ocean_dat_1990s, dat, 'Oxygen')
ave_count += a
ave_oxygen += b

a, b = ocean_jellyfish_conbine(jellyfish_1980s, ocean_dat_1980s, dat, 'Oxygen')
ave_count += a
ave_oxygen += b

a, b = ocean_jellyfish_conbine(jellyfish_1970s, ocean_dat_1970s, dat, 'Oxygen')
ave_count += a
ave_oxygen += b

a, b = ocean_jellyfish_conbine(jellyfish_1960s, ocean_dat_1960s, dat, 'Oxygen')
ave_count += a
ave_oxygen += b

a, b = ocean_jellyfish_conbine(jellyfish_1950s, ocean_dat_1950s, dat, 'Oxygen')
ave_count += a
ave_oxygen += b
# Remove the outlier 
ave_count_1 = []
ave_oxygen_1 = []
for i in range(len(ave_salinity)):
    if ave_count[i] < 140000:
        ave_count_1.append(ave_count[i])
        ave_oxygen_1.append(ave_oxygen[i])
# scatter plot 
sns.set(style = 'darkgrid')
g = sns.jointplot(ave_oxygen_1, ave_count_1)
g = g.plot(sns.regplot, sns.distplot)
g.set_axis_labels('Oxygen', 'Jelly Fish Average Count')
g.annotate(stats.pearsonr)
g.savefig('jellyfish_Oxygen.png')

#%%
#################################################################
# collect and conbine average phosphate and average count for   #
# different decades and do the plotting                         #
#################################################################

# collect ave_phos and ave_count 
ave_count = []
ave_phos = []

a, b = ocean_jellyfish_conbine(jellyfish_2010s, ocean_dat_2010s, dat, 'Phosphate')
ave_count += a
ave_phos += b

a, b = ocean_jellyfish_conbine(jellyfish_2000s, ocean_dat_2000s, dat, 'Phosphate')
ave_count += a
ave_phos += b

a, b = ocean_jellyfish_conbine(jellyfish_1990s, ocean_dat_1990s, dat, 'Phosphate')
ave_count += a
ave_phos += b

a, b = ocean_jellyfish_conbine(jellyfish_1980s, ocean_dat_1980s, dat, 'Phosphate')
ave_count += a
ave_phos += b

a, b = ocean_jellyfish_conbine(jellyfish_1970s, ocean_dat_1970s, dat, 'Phosphate')
ave_count += a
ave_phos += b

a, b = ocean_jellyfish_conbine(jellyfish_1960s, ocean_dat_1960s, dat, 'Phosphate')
ave_count += a
ave_phos += b

a, b = ocean_jellyfish_conbine(jellyfish_1950s, ocean_dat_1950s, dat, 'Phosphate')
ave_count += a
ave_phos += b
# Remove the outlier 
ave_count_1 = []
ave_phos_1 = []
for i in range(len(ave_phos)):
    if ave_count[i] < 140000:
        ave_count_1.append(ave_count[i])
        ave_phos_1.append(ave_phos[i])
# scatter plot 
sns.set(style = 'darkgrid')
g = sns.jointplot(ave_phos_1, ave_count_1)
g = g.plot(sns.regplot, sns.distplot)
g.set_axis_labels('Phosphate', 'Jelly Fish Average Count')
g.annotate(stats.pearsonr)
g.savefig('jellyfish_Phosphate.png')
#%%
#################################################################
# collect and conbine average nitrate and average count for     #
# different decades and do the plotting                         #
#################################################################

# collect ave_nitrate and ave_count 
ave_count = []
ave_nitrate = []

a, b = ocean_jellyfish_conbine(jellyfish_2010s, ocean_dat_2010s, dat, 'Nitrate')
ave_count += a
ave_nitrate += b

a, b = ocean_jellyfish_conbine(jellyfish_2000s, ocean_dat_2000s, dat, 'Nitrate')
ave_count += a
ave_nitrate += b

a, b = ocean_jellyfish_conbine(jellyfish_1990s, ocean_dat_1990s, dat, 'Nitrate')
ave_count += a
ave_nitrate += b

a, b = ocean_jellyfish_conbine(jellyfish_1980s, ocean_dat_1980s, dat, 'Nitrate')
ave_count += a
ave_nitrate += b

a, b = ocean_jellyfish_conbine(jellyfish_1970s, ocean_dat_1970s, dat, 'Nitrate')
ave_count += a
ave_nitrate += b

a, b = ocean_jellyfish_conbine(jellyfish_1960s, ocean_dat_1960s, dat, 'Nitrate')
ave_count += a
ave_nitrate += b

a, b = ocean_jellyfish_conbine(jellyfish_1950s, ocean_dat_1950s, dat, 'Nitrate')
ave_count += a
ave_nitrate += b
# Remove the outlier 
ave_count_1 = []
ave_nitrate_1 = []
for i in range(len(ave_nitrate)):
    if ave_count[i] < 140000:
        ave_count_1.append(ave_count[i])
        ave_nitrate_1.append(ave_nitrate[i])
# scatter plot 
sns.set(style = 'darkgrid')
g = sns.jointplot(ave_nitrate_1, ave_count_1)
g = g.plot(sns.regplot, sns.distplot)
g.set_axis_labels('Nitrate', 'Jelly Fish Average Count')
g.annotate(stats.pearsonr)
g.savefig('jellyfish_Nitrate.png')

#%%
#################################################################
# collect and conbine average pH and average count for          #
# different decades and do the plotting                         #
#################################################################

# collect ave_pH and ave_count 
ave_count = []
ave_pH = []

a, b = ocean_jellyfish_conbine(jellyfish_2010s, ocean_dat_2010s, dat, 'pH')
ave_count += a
ave_pH += b

a, b = ocean_jellyfish_conbine(jellyfish_2000s, ocean_dat_2000s, dat, 'pH')
ave_count += a
ave_pH += b

a, b = ocean_jellyfish_conbine(jellyfish_1990s, ocean_dat_1990s, dat, 'pH')
ave_count += a
ave_pH += b

a, b = ocean_jellyfish_conbine(jellyfish_1980s, ocean_dat_1980s, dat, 'pH')
ave_count += a
ave_pH += b

a, b = ocean_jellyfish_conbine(jellyfish_1970s, ocean_dat_1970s, dat, 'pH')
ave_count += a
ave_pH += b

a, b = ocean_jellyfish_conbine(jellyfish_1960s, ocean_dat_1960s, dat, 'pH')
ave_count += a
ave_pH += b

a, b = ocean_jellyfish_conbine(jellyfish_1950s, ocean_dat_1950s, dat, 'pH')
ave_count += a
ave_pH += b
# Remove the outlier 
ave_count_1 = []
ave_pH_1 = []
for i in range(len(ave_pH)):
    if ave_count[i] < 140000:
        ave_count_1.append(ave_count[i])
        ave_pH_1.append(ave_pH[i])
# scatter plot 
sns.set(style = 'darkgrid')
g = sns.jointplot(ave_pH_1, ave_count_1)
g = g.plot(sns.regplot, sns.distplot)
g.set_axis_labels('pH', 'Jelly Fish Average Count')
g.annotate(stats.pearsonr)
g.savefig('jellyfish_pH.png')