# Data Wrangling Workflow

## Non-Biological Data:
To go through the process of scraping the data from the OSD reports/casts,
Follow the following steps:
- Download the files Data_1.csv, Data_2.csv, ..., Data_16.csv from the Google Drive (check the main README file of the repo)
- Make sure you use the scripts below to read the data. The csv files mentioned above are not regular csv files. They conatin WOD reports/casts and are not tabular data seperated by commas.
- Run the script: reading_wod_data_script.py, then
- Run the script: data_cleaning.py, then
- Run the script: splitting_by_decade.py, then
- To check that you split the data correctly by decade, run: checking_decades_distributed_properly.py, then
- Run the script: Day_night_measurement_step_1.py, then
- Run the script: Day_night_measurement_step_2.py, then
- Run the script: generate_data_depth_0.py (This will generate the data at depth 0, which is used in the Tempearture Trends Analysis - check Analysis/Trends folder of the repo)

## Biological Data:
To go through the process of scraping the data from the OSD reports/casts of biological data,
Follow the following steps:
- Download the files Data_1.csv, Data_2.csv, ..., Data_16.csv from the Google Drive (check the main README file of the repo)
- Run the script: reading_wod_biological_data_script.py, then
- Run the script: data_cleaning_biological.py, then
- Run the script: splitting_by_decade_biological.py.

## Jellyfish Data:
To acquire the Jellyfish data run the script: read_jellyfish_data.py
