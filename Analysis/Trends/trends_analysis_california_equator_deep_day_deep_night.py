# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 02:16:39 2019

@author: albat
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
num_or_yr_th = 2

# Summer Days
df_lat = df[(df['Year'] < 2010) & (df['Year'] > 1960) &\
            (df['Month'] > 6) & (df['Month'] < 9) & \
            (df['deep_day_night'] == 'dd')]\
            .groupby(['Latitude_app','Longitude_app'])['Year'].nunique().to_frame()

df_lat_2 = df_lat[df_lat['Year'] > num_or_yr_th].copy()
coordinate_list = list(df_lat_2.index)

# We need to change the type to string because pandas save tuples as strings in columns
coordinate_list2 = [str(i) for i in coordinate_list]

df_smer_day = df[(df['Month'] > 6) & (df['Month'] < 9) &\
                 (df['deep_day_night'] == 'dd') & \
                 (df['coordinates'].isin(coordinate_list2))].copy()

# Summer Nights
df_lat = df_lat = df[(df['Year'] < 2010) & (df['Year'] > 1960) &\
            (df['Month'] > 6) & (df['Month'] < 9) & \
            (df['deep_day_night'] == 'dn')]\
            .groupby(['Latitude_app','Longitude_app'])['Year'].nunique().to_frame()
df_lat_2 = df_lat[df_lat['Year'] > num_or_yr_th].copy()

coordinate_list = list(df_lat_2.index)

# We need to change the type to string because pandas save tuples as strings in columns
coordinate_list2 = [str(i) for i in coordinate_list]

df_smer_nit = df[(df['Month'] > 6) & (df['Month'] < 9) &\
                 (df['deep_day_night'] == 'dn') & \
                 (df['coordinates'].isin(coordinate_list2))].copy()


#%% California Baby ;)

# ------------------------- Line Plots

df_smer_day_mean = df_smer_day[(df_smer_day['Latitude'] > 31) & (df_smer_day['Latitude'] < 34) &\
                               (df_smer_day['Longitude'] < -115) & (df_smer_day['Longitude'] > - 120)].groupby(['Year']).Temperatur.mean()

df_smer_nit_mean = df_smer_nit[(df_smer_nit['Latitude'] > 31) & (df_smer_nit['Latitude'] < 34) &\
                               (df_smer_nit['Longitude'] < -115) & (df_smer_nit['Longitude'] > - 120)].groupby(['Year']).Temperatur.mean()

df_smer_day_mean1 = df_smer_day[(df_smer_day['Latitude'] > 36) & (df_smer_day['Latitude'] < 40) &\
                               (df_smer_day['Longitude'] < -121) & (df_smer_day['Longitude'] > - 124)].groupby(['Year']).Temperatur.mean()

df_smer_nit_mean1 = df_smer_nit[(df_smer_nit['Latitude'] > 36) & (df_smer_nit['Latitude'] < 40) &\
                               (df_smer_nit['Longitude'] < -121) & (df_smer_nit['Longitude'] > - 124)].groupby(['Year']).Temperatur.mean()



g3 = plt.figure(figsize=(12,5))
plt.xlabel('Year', fontsize=18)
plt.ylabel('Average Temperature', fontsize=18)
plt.title('Southern/Northern California Average Temperature Vs. Year', fontsize=18)

ax1 = df_smer_day_mean.rolling(5, center = False).mean().plot(color='orange', grid=True, secondary_y=False, label='During Day')
ax2 = df_smer_nit_mean.rolling(5, center = False).mean().plot(color='blue', grid=True, secondary_y=False, label='During Night')

ax3 = df_smer_day_mean1.rolling(5, center = False).mean().plot(color='orange', grid=True, secondary_y=False)
ax4 = df_smer_nit_mean1.rolling(5, center = False).mean().plot(color='blue', grid=True, secondary_y=False)

ax1.tick_params(axis="x", labelsize=16)
ax1.tick_params(axis="y", labelsize=16)

h1, l1 = ax1.get_legend_handles_labels()

ax1.set_xlim(1965,2005)
ax1.set_ylim(10,25)

plt.legend(h1, l1, loc=2, fontsize=16)
plt.show()

#%% Equator Baby ;)

# ------------------------- Line Plots

df_smer_day_mean = df_smer_day[(df_smer_day['Latitude'] > -2) & (df_smer_day['Latitude'] < 2) &\
                               (df_smer_day['Longitude'] < 180) & (df_smer_day['Longitude'] > - 180)].groupby(['Year']).Temperatur.mean()

df_smer_nit_mean = df_smer_nit[(df_smer_nit['Latitude'] > -2) & (df_smer_nit['Latitude'] < 2) &\
                               (df_smer_nit['Longitude'] < 180) & (df_smer_nit['Longitude'] > - 180)].groupby(['Year']).Temperatur.mean()


g3 = plt.figure(figsize=(12,5))
plt.xlabel('Year', fontsize=18)
plt.ylabel('Average Temperature', fontsize=18)
plt.title('Equator Average Temperature Vs. Year', fontsize=18)

ax1 = df_smer_day_mean.rolling(5, center = False).mean().plot(color='orange', grid=True, secondary_y=False, label='During Day')
ax2 = df_smer_nit_mean.rolling(5, center = False).mean().plot(color='blue', grid=True, secondary_y=False, label='During Night')

ax1.tick_params(axis="x", labelsize=16)
ax1.tick_params(axis="y", labelsize=16)

h1, l1 = ax1.get_legend_handles_labels()

ax1.set_xlim(1965,2005)
ax1.set_ylim(20,30)

plt.legend(h1, l1, loc=2, fontsize=16)
plt.show()

# =============================================================================
# #%% Arctic
# df_smer_day_mean = df_smer_day[(df_smer_day['Latitude'] > 70) & (df_smer_day['Latitude'] < 70) &\
#                                (df_smer_day['Longitude'] < 180) & (df_smer_day['Longitude'] > - 180)].groupby(['Year']).Temperatur.mean()
# 
# df_smer_nit_mean = df_smer_nit[(df_smer_nit['Latitude'] > 75) & (df_smer_nit['Latitude'] < 78) &\
#                                (df_smer_nit['Longitude'] < 180) & (df_smer_nit['Longitude'] > - 180)].groupby(['Year']).Temperatur.mean()
# 
# 
# g3 = plt.figure(figsize=(12,5))
# plt.xlabel('Year', fontsize=18)
# plt.ylabel('Average Temperature', fontsize=18)
# plt.title('Arctic Average Temperature Vs. Year', fontsize=18)
# 
# ax1 = df_smer_day_mean.rolling(5, center = False).mean().plot(color='orange', grid=True, secondary_y=False, label='During Day')
# ax2 = df_smer_nit_mean.rolling(5, center = False).mean().plot(color='blue', grid=True, secondary_y=False, label='Equator')
# 
# ax1.tick_params(axis="x", labelsize=16)
# ax1.tick_params(axis="y", labelsize=16)
# 
# h1, l1 = ax1.get_legend_handles_labels()
# 
# ax1.set_xlim(1965,2005)
# ax1.set_ylim(-5,10)
# 
# plt.legend(h1, l1, loc=2, fontsize=16)
# plt.show()
# =============================================================================








