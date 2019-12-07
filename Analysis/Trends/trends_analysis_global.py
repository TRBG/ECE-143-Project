
"""
Analysis of Global Summer Days (Deep Day) Temperatures Trends

"""
import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="darkgrid")

#%% Reading the data and choosing a certain depth (for now depth = 0)
    
start = time.time()
df = pd.read_csv('all_data_depth_0_temp_nan_free_coordinates.csv')
    
end = time.time()
print('The time for to read the dataframe: ' +\
      str(round(end - start,2)) + ' seconds')

#%%
#=============================================================================#
#=============================================================================#
#=============================================================================#
#=============================================================================#
    ### Temperature Trends - Summer Days
#=============================================================================#
#=============================================================================#
#=============================================================================#
#=============================================================================#

 
#%%
num_or_yr_th = 48

# Summer Days
df_lat = df[(df['Year'] < 2010) & (df['Year'] > 1960) &\
            (df['Month'] > 6) & (df['Month'] < 9) & \
            (df['day_night'] == 'd')]\
            .groupby(['Latitude_app','Longitude_app'])['Year'].nunique().to_frame()

df_lat_2 = df_lat[df_lat['Year'] > num_or_yr_th].copy()
coordinate_list = list(df_lat_2.index)

# We need to change the type to string because pandas save tuples as strings in columns
coordinate_list2 = [str(i) for i in coordinate_list]

df_smer_day = df[(df['Month'] > 6) & (df['Month'] < 9) &\
                 (df['day_night'] == 'd') & \
                 (df['coordinates'].isin(coordinate_list2))].copy()

num_or_yr_th = 40
# Summer Nights
df_lat = df[(df['Year'] < 2010) & (df['Year'] > 1960) &\
            (df['Month'] > 6) & (df['Month'] < 9) & \
            (df['day_night'] == 'n')]\
            .groupby(['Latitude_app','Longitude_app'])['Year'].nunique().to_frame()

df_lat_2 = df_lat[df_lat['Year'] > num_or_yr_th].copy()
coordinate_list = list(df_lat_2.index)

# We need to change the type to string because pandas save tuples as strings in columns
coordinate_list2 = [str(i) for i in coordinate_list]

df_smer_nit = df[(df['Month'] > 6) & (df['Month'] < 9) &\
                 (df['day_night'] == 'n') & \
                 (df['coordinates'].isin(coordinate_list2))].copy()


#%% north Hemisphere
df_smer_day_mean = df_smer_day[(df_smer_day['Latitude'] > 0) & (df_smer_day['Latitude'] < 90) &\
                               (df_smer_day['Longitude'] < 180) & (df_smer_day['Longitude'] > - 180)].groupby(['Year']).Temperatur.mean()

df_smer_nit_mean = df_smer_nit[(df_smer_nit['Latitude'] > 0) & (df_smer_nit['Latitude'] < 90) &\
                               (df_smer_nit['Longitude'] < 180) & (df_smer_nit['Longitude'] > - 180)].groupby(['Year']).Temperatur.mean()


g3 = plt.figure(figsize=(12,5))
plt.xlabel('Year', fontsize=18)
plt.ylabel('Average Temperature', fontsize=18)
plt.title('Global Average Temperature Vs. Year', fontsize=18)

ax1 = df_smer_day_mean.rolling(5, center = False).mean().plot(color='orange', grid=True, secondary_y=False, label='During Day')
ax2 = df_smer_nit_mean.rolling(5, center = False).mean().plot(color='blue', grid=True, secondary_y=False, label='During Night')

ax1.tick_params(axis="x", labelsize=16)
ax1.tick_params(axis="y", labelsize=16)

h1, l1 = ax1.get_legend_handles_labels()

ax1.set_xlim(1965,2005)
ax1.set_ylim(10,30)

plt.legend(h1, l1, loc=2, fontsize=16)
plt.show()








