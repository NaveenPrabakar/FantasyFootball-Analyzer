import os
import io

import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from pymongo import MongoClient


MONGO_URI = os.getenv("Mongo_URI")
client = MongoClient(MONGO_URI)
db = client['data_analysis']
collection = db['nfl_files']



#Make areas to save the graphs

if not os.path.exists("saved_graphs"):
    os.makedirs("saved_graphs")




def get_data(playername):

    names = []


    #Get the data needed
    document = collection.find_one({'_id': 'nfl_stats'})
    retrieved_df = pd.DataFrame(document['data'])


    df = clean_data(retrieved_df)

    names.append(td_vs_int(df, playername))

    return names
    




#To intially clean the filtered qb data
def clean_data(df):

    filtered_data = df[df['Season'].str.isdigit()]
    filtered_data.reset_index(drop=True, inplace=True)


    return filtered_data



#One graph
def td_vs_int(df, playername):

    # Plotting Touchdowns vs. Interceptions
    plt.figure(figsize=(10, 6))
    plt.plot(df['Season'], df['TD'], label='Touchdowns', marker='o', linestyle='-')
    plt.plot(df['Season'], df['Int'], label='Interceptions', marker='x', linestyle='-')

    # Customize the chart
    plt.title('Touchdowns vs. Interceptions', fontsize=14)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Count', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    plot_file_path = f'saved_graphs/{playername}.png'
    plt.savefig(plot_file_path)

    return plot_file_path


 













