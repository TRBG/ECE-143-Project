"""
#########################################################################################################################
##Reading csv data files and merge them into a single Dataframe using "CAST" number 
##and filnally saving the merged Dataframe into a single csv file
#########################################################################################################################
"""
import os
import time
import datetime
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import plotly.express as px
import matplotlib.pyplot as plt

decades = ['1950','1960','1970','1980','1990','2000','2010']
all_bio_data = pd.DataFrame()
all_geo_data = pd.DataFrame()
### Reading all the biological and non_bio csv files and append them into two dataframe.
for i in decades: 
    start = time.time()
    wd = os.getcwd() 
    bio_data_fname = wd + '/DataFiles/cleaned_biological_data_of_the' + i + 's.csv'
    geo_data_fname = wd + '/DataFiles/cleaned_data_of_the' + i + 's.csv'
    bio_data = pd.read_csv(bio_data_fname)
    geo_data = pd.read_csv(geo_data_fname)
    all_bio_data = all_bio_data.append(bio_data)
    all_geo_data = all_geo_data.append(geo_data)
### Merge two dataframe (bio and none_bio) into a single dataframe based on the "CAST" column.
merged = all_bio_data.merge(all_geo_data, on='CAST')

#### Save resulting Dataframe into a single csv file for the future use.
merged.to_csv( wd + '/DataFiles/all_bio_geo_merged.csv')


#%%
"""
#########################################################################################################################
##Using erddap protocol to connect to a noaa server and retrive the plankton database, and save it into a single csv file 
##for the future use.
#########################################################################################################################
"""
import os
import pandas as pd
from erddapy import ERDDAP


#https://coastwatch.pfeg.noaa.gov/erddap/info/wocecpr/index.html
### initializing the erddap class instance with the data server address and the connection protocol.
e = ERDDAP(
  server='https://coastwatch.pfeg.noaa.gov/erddap',
  protocol='tabledap',
)
### specifying the data format of the response.
e.response = 'csv'
### specifying the database name we need the data from.
e.dataset_id = 'wocecpr'
### specifying the data constraints
e.constraints = {
    'time>=': '2000-01-15T01:24:00Z',
    'time<=': '2010-01-17T13:39:00Z', 
    
    'latitude>=': 37.0,
    'latitude<=': 43.43,
    'longitude>=': 317.56,
    'longitude<=': 322.87,
}
###specifying the variables(columns name) to be retrived.
e.variables = [
    'sample',
    'latitude',
    'longitude',
    'life_stage',
    'abundance',
    'time',
]
### searching for the server link and doing the handshaking process.
search_url = e.get_search_url(response = 'csv')
### receiving requested data and saving it into a dataframe
search = pd.read_csv(search_url)
df = e.to_pandas()
### receiving current working directory and saving the dataframe into a single csv file in that path.
wd = os.getcwd() 
df.to_csv( wd + '/DataFiles/plankton_swocecpr.csv')


#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based on Depth and total wet mass and place a point regarding 
##for each data point lon and lat into a map.
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import plotly.express as px

wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
df = pd.read_csv(fname)
d= df[['Latitude_x', 'Longitude_x', 'Temperatur', 'Total Wet Mass', 'Depth']] 
d = d[(d['Total Wet Mass'] > 0.0) & (d['Depth'] == 0)]
d = d.dropna()
fig = px.scatter_mapbox(d, lat="Latitude_x", lon="Longitude_x", color="Total Wet Mass", size="Total Wet Mass", zoom=1, height=300, )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based on planktons displacement volume and place a point regarding 
##for each data point lon and lat into a map.
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import plotly.express as px

wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
df = pd.read_csv(fname)
d= df[['Latitude_x', 'Longitude_x', 'Temperatur', 'Displacemnt Vol']] 
d = d[d['Displacemnt Vol'] > 0]
d = d.dropna()
fig = px.scatter_mapbox(d, lat="Latitude_x", lon="Longitude_x", color="Displacemnt Vol", size="Displacemnt Vol", zoom=1, height=300, )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based on planktons time of the sampling (night) and place a point regarding 
##for each data point lon and lat into a map.
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import plotly.express as px

wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
df = pd.read_csv(fname)
d= df[['latitude (degrees_north)', 'longitude (degrees_east)', 'abundance (per 100 cubic meters)', 'time (UTC)']] 
d = d[d['abundance (per 100 cubic meters)'] > 0]
time_utc = d['time (UTC)'].tolist()
hour = [pd.to_datetime(i).hour for i in time_utc]
d["hour"] = hour
d.to_csv("/Users/omid/Desktop/ECE143/DataFiles/plankton_swocecpr__hour_00_10.csv")
d = d[(d['hour'] > 0) & (d['hour'] < 6) | (d['hour'] > 18)]
d.dropna()
fig = px.scatter_mapbox(d, lat="latitude (degrees_north)", lon="longitude (degrees_east)", color="abundance (per 100 cubic meters)", size="abundance (per 100 cubic meters)", zoom=3, height=300, )
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based depth zero and draw a 
## correlation graph Y = Total Wet Mass and X = Temperature
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
## returning the current working directory
wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
## opening the csv file into a pandas dataframe from current working directory
df = pd.read_csv(fname)
## selecting required columns fro dataframe
d= df[['Temperatur', 'Total Wet Mass','Depth',  'Latitude_x', 'Longitude_x']] 
## filtering data based on depth
d = d[(d['Total Wet Mass'] < 500) &(d['Depth'] == 0)]
## droping all duplicated/NotANumber rows
d = d.drop_duplicates()
d = d.dropna()
sns.set(style='darkgrid')
## plotting correlation plot
g = sns.JointGrid(x="Temperatur", y="Total Wet Mass", data=d)
g = g.plot(sns.regplot, sns.distplot)  
g.annotate(stats.pearsonr)
## setting axis lables
g.set_axis_labels('Temperatur', 'Planktons Wet Mass')
plt.show()

#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based depth zero and draw a 
## correlation graph Y = Total Wet Mass and X = Salinity
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
## returning the current working directory
wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
## opening the csv file into a pandas dataframe from current working directory
df = pd.read_csv(fname)
## selecting required columns fro dataframe
d= df[['Salinity', 'Total Wet Mass','Depth',  'Latitude_x', 'Longitude_x']] 
## filtering data based on depth
d = d[(d['Total Wet Mass'] < 500) &(d['Depth'] == 0) & (d['Salinity'] > 0)]
## droping all duplicated/NotANumber rows
d = d.drop_duplicates()
d = d.dropna()
sns.set(style='darkgrid')
## plotting correlation plot
g = sns.JointGrid(x="Salinity", y="Total Wet Mass", data=d)
g = g.plot(sns.regplot, sns.distplot)  
g.annotate(stats.pearsonr)
## setting axis lables
g.set_axis_labels('Salinity', 'Planktons Wet Mass')
plt.show()

#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based depth zero and draw a 
## correlation graph Y = Total Wet Mass and X = Oxygen
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
## returning the current working directory
wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
## opening the csv file into a pandas dataframe from current working directory
df = pd.read_csv(fname)
## selecting required columns fro dataframe
d= df[['Oxygen', 'Total Wet Mass','Depth',  'Latitude_x', 'Longitude_x']] 
## filtering data based on depth
d = d[(d['Total Wet Mass'] < 500) &(d['Depth'] == 0) & (d['Oxygen'] > 0)]
## droping all duplicated/NotANumber rows
d = d.drop_duplicates()
d = d.dropna()
sns.set(style='darkgrid')
## plotting correlation plot
g = sns.JointGrid(x="Oxygen", y="Total Wet Mass", data=d)
g = g.plot(sns.regplot, sns.distplot)  
g.annotate(stats.pearsonr)
## setting axis lables
g.set_axis_labels('Oxygen', 'Planktons Wet Mass')
plt.show()

#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based depth zero and draw a 
## correlation graph Y = Total Wet Mass and X = Phosphate
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
## returning the current working directory
wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
## opening the csv file into a pandas dataframe from current working directory
df = pd.read_csv(fname)
## selecting required columns fro dataframe
d= df[['Phosphate', 'Total Wet Mass','Depth',  'Latitude_x', 'Longitude_x']] 
## filtering data based on depth
d = d[(d['Total Wet Mass'] < 500) &(d['Depth'] == 0) & (d['Phosphate'] > 0)]
## droping all duplicated/NotANumber rows
d = d.drop_duplicates()
d = d.dropna()
sns.set(style='darkgrid')
## plotting correlation plot
g = sns.JointGrid(x="Phosphate", y="Total Wet Mass", data=d)
g = g.plot(sns.regplot, sns.distplot)  
g.annotate(stats.pearsonr)
## setting axis lables
g.set_axis_labels('Phosphate', 'Planktons Wet Mass')
plt.show()
#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based depth zero and draw a 
## correlation graph Y = Total Wet Mass and X = pH
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
## returning the current working directory
wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
## opening the csv file into a pandas dataframe from current working directory
df = pd.read_csv(fname)
## selecting required columns fro dataframe
d= df[['pH', 'Total Wet Mass','Depth',  'Latitude_x', 'Longitude_x']] 
## filtering data based on depth
d = d[(d['Depth'] == 0) & (d['pH'] > 0)]
## droping all duplicated/NotANumber rows
d = d.drop_duplicates()
d = d.dropna()
sns.set(style='darkgrid')
## plotting correlation plot
g = sns.JointGrid(x="pH", y="Total Wet Mass", data=d)
g = g.plot(sns.regplot, sns.distplot)  
g.annotate(stats.pearsonr)
## setting axis lables
g.set_axis_labels('pH', 'Planktons Wet Mass')
plt.show()
#%%
"""
#########################################################################################################################
##Read the bio/none_bio datafile for plankton data and filter them based depth zero and draw a 
## correlation graph Y = Total Wet Mass and X = Nitrate
#########################################################################################################################
"""
import os
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
## returning the current working directory
wd = os.getcwd() 
fname =  wd + '/DataFiles/all_bio_geo_merged.csv'
## opening the csv file into a pandas dataframe from current working directory
df = pd.read_csv(fname)
## selecting required columns fro dataframe
d= df[['Nitrate', 'Total Wet Mass','Depth',  'Latitude_x', 'Longitude_x']] 
## filtering data based on depth
d = d[(d['Total Wet Mass'] < 500) & (d['Depth'] == 0) & (d['Nitrate'] > 0)]
## droping all duplicated/NotANumber rows
d = d.drop_duplicates()
d = d.dropna()
sns.set(style='darkgrid')
## plotting correlation plot
g = sns.JointGrid(x="Nitrate", y="Total Wet Mass", data=d)
g = g.plot(sns.regplot, sns.distplot)  
g.annotate(stats.pearsonr)
## setting axis lables
g.set_axis_labels('Nitrate', 'Planktons Wet Mass')
plt.show()