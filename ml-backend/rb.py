import os
import aws

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from pymongo import MongoClient


MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['data_analysis']
collection = db['nfl_files']



#Make areas to save the graphs

if not os.path.exists("saved_graphs"):
    os.makedirs("saved_graphs")

if not os.path.exists("/tmp/saved_graphs"):
    os.makedirs("/tmp/saved_graphs")



def get_data(playername):

    names = []


    #Get the data needed
    document = collection.find_one({'_id': 'nfl_stats'})
    retrieved_df = pd.DataFrame(document['data'])


    df = clean_data(retrieved_df)

    names.append(td_vs_int(df, playername))
    names.append(bar(df, playername))
    names.append(last(playername, df))


    return names

def rb_td(df, playername):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Season', y='Y/A', data=retrieved_df, marker='o')
    plt.title('Derrick Henry Yards Per Carry per Season')
    plt.xlabel('Season')
    plt.ylabel('Yards Per Carry')
    plt.grid(True)
    plt.tight_layout()

    plot_file_path = f"saved_graphs/{playername}.png"
    plt.savefig(plot_file_path)

    aws.upload_file(f"saved_graphs/{playername}.png", "nflfootballwebsite", f"{playername}.png")

    return plot_file_path 