#%%
##################################################
# Transform the jellyfish data from .mat to .csv #
# and reduce the jellyfish data                  #
##################################################

def read_jellyfish_data():
    '''This fuction transfroms the jelly fish data from .mat to .csv
    '''
    import scipy.io
    import csv
    import pandas as pd

    mat = scipy.io.loadmat('jelly_fish.mat')
    fieldname = ['project_title', 'owner_dataset', 'contact', 'location_name', 'date',
                 'year', 'month', 'day', 'time_local', 'lat', 'lon', 'taxon', 'rank_phylum', 
                 'rank_class', 'rank_order', 'rank_family', 'rank_genus', 'rank_species',
                 'data_type', 'collection_method', 'net_opening', 'net_mesh', 'depth',
                 'depth_upper', 'depth_lower', 'count_actual', 'density', 'density_integrated',
                 'biovolume', 'biovolume_integrated', 'weight_wet', 'weight_dry', 'presence_absence',
                 'study_type', 'accompanying_ancillary_data', 'catch_per_effort', 'sub_project_title']         
    del mat['__globals__'], mat['__header__'], mat['__version__']
    df = pd.DataFrame(mat)
    df = df[fieldname]
    df.to_csv('jelly_fish.csv')
# read the jelly_fish.mat file and save as jelly_fish.csv
read_jellyfish_data()
# reduce the jelly fish data and save it as jelly_fish_reduced
import pandas as pd
df = pd.read_csv('jelly_fish.csv')
a = df[['year','month', 'lat', 'lon', 'count_actual', 'density']]
b = a[a['year'] >= 1950] 
b.to_csv('jelly_fish_reduced.csv')




# %%
