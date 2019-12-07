# ECE-143-Project
This repo contains the code, data, and approach for the ECE 143 Project at UCSD

In order to complete this project, we used following databases
# Datasets: 

### * NOAA National Centers for Environmental Information [ WOD (World Ocean Database )](https://www.nodc.noaa.gov/OC5/SELECT/dbsearch/dbsearch.html)
      	 3.2 million Casts
      	 250 Thousand Biological Casts
This database was acquired through a request by form from the provided website.
 
Data for non_biological ocean variables including temperature, salinity, oxygen, Phosphate, pH, nitrate etc.

### * BCO-DMO (Biological & Chemistry Oceanography Data Management Office) [JeDI](https://www.bco-dmo.org/dataset/526852)

Data for jellyfish and zooplanktons
### * NOAA Coast Watch Environmental Data [wocecpr](https://coastwatch.pfeg.noaa.gov/erddap/info/wocecpr/index.html)
Data for zooplanktons
This database was acquired from the server using following method
### [ERDDAP (Environmental Research Divisions Data Access Program)](https://upwell.pfeg.noaa.gov/erddap/index.html)
ERDDAP is a data server that gives you a simple, consistent way to download subsets of scientific datasets in common file formats and make graphs and maps. This ERDDAP installation makes all of the datasets in the NOAA-wide UAF THREDDS catalog and many additional datasets available via ERDDAP.



## All the datafiles are stored in a google drive and are accessable using this [link](https://drive.google.com/open?id=1zReO31KMWB2_QQf4wpbK94Cvntt6SRyd)

# Github File/Folder Organization:
      .
      ├── Analysis                                            # All the related analysis python codes 
      │    ├── Non_biological                                  # Analysis python codes related to Non_biological variables
      │    │    ├── scatter_nitrate_Oxygen.py
      │    │    ├── scatter_nitrate_temperature.py
      │    │    ├── scatter_Oxygen_temperature.py
      │    │    ├── scatter_pH_Oxygen.py
      │    │    ├── scatter_pH_temperature.py
      │    │    ├── scatter_phosphate_Oxygen_depth10.py
      │    │    ├── scatter_phosphate_Oxygen.py
      │    │    └── scatter_phosphate_temperature.py
      │    └── Biological                                      # Analysis python codes related to Biological variables
      │         ├── Planktons.py                               # Correlation analysis for Planktons and ocean data
      │         └── jellyfish_measurments_scatter.py           # Correlation analysis for Jellyfish and ocean data
      ├── Data_Wrangling                                      # Python code to acquire/clean the data 
      │     ├── Data_Wrangling_Instructions.md 
      │     ├── Day_night_measurment_step_1.py
      │     ├── Day_night_measurment_step_2.py
      │     ├── checking_decades_distributed_properly.py
      │     ├── data_cleaning.py
      │     ├── generate_data_depth_0.py
      │     ├── read_jellyfish_data.py
      │     ├── read_ocean_data.py
      │     ├── reading_wod_data_script.py
      │     └── splitting_by_decade.py
      │
      ├── ProjectVisualization.ipynb                          # Jupiter notebook file for all the plots in the presentation
      ├── 143project_slides_group11.pptx                      # Presentation slides
      └── README.md                                           # Readme files

# Modules/Packages used in the codes:
      import os
      import time
      import math
      import datetime
      import numpy as np
      import pandas as pd
      import seaborn as sns
      import scipy 
      import plotly.express as px
      import matplotlib.pyplot as plt
      import erddapy 
      import suntime
      import csv
      


