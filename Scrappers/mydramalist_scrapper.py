from Scrappers.scrap_functions import *
import pandas as pd

# Getting the tags of popular dramas.
drama_tags = mydramalist_tags_popular()

# Storing the drama reference tags in a csv for later use.
drama_tags_list = list(drama_tags)
drama_tags_list_file = "Scrappers/Scrappers_files/drama_tags_list.csv"
drama_df = pd.DataFrame(data={'drama_tags_list': drama_tags_list})
drama_df.to_csv(drama_tags_list_file, sep=',', index = False)

# Creating the database for a chunk of dramas.
start_idx = 0
stop_idx = 12
drama_DB = mydramalist_createDB(drama_tags_list_file, start_idx, stop_idx)

# Storing the database in a csv.
drama_DB.to_csv(f'Scrappers/Scrappers_files/mydramalist_reviews_{start_idx}_to_{stop_idx}')