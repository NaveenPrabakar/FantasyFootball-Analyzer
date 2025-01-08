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

def bar(df, playername):
    # Define the data manually based on the uploaded image
    data = {
        'Season': ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
        'Rushing Yards': [490, 744, 1059, 1540, 2027, 937, 1538, 1167, 1783],
        'Scrimmage Yards': [627, 880, 1158, 1746, 2141, 1091, 1936, 1381, 1953]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    #  Create the bar graph
    plt.figure(figsize=(12, 6))
    bar_width = 0.4
    x = range(len(df['Season']))

    # Plot Rushing Yards
    plt.bar(x, df['Rushing Yards'], width=bar_width, label='Rushing Yards', color='blue')

    # Plot Scrimmage Yards next to Rushing Yards
    plt.bar([i + bar_width for i in x], df['Scrimmage Yards'], width=bar_width, label='Scrimmage Yards', color='orange')

    # Customize the chart
    plt.title('Rushing Yards and Scrimmage Yards Per Season for Derrick Henry', fontsize=16)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Yards', fontsize=12)
    plt.xticks([i + bar_width / 2 for i in x], df['Season'], rotation=45)  # Center x-ticks
    plt.legend()
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    plot_file_path = f"saved_graphs/{playername}.png"
    plt.savefig(plot_file_path)

    aws.upload_file(f"saved_graphs/{playername}.png", "nflfootballwebsite", f"{playername}.png")

    return plot_file_path 

def last(df, playername):
    data = {
    'Season': ['2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024'],
    'Total Touchdowns': [5, 6, 12, 18, 17, 10, 13, 12, 16]  # Combine rushing + receiving TDs from the dataset
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Create the line graph for Total Touchdowns
    plt.figure(figsize=(12, 6))
    plt.plot(df['Season'], df['Total Touchdowns'], marker='o', linestyle='-', color='purple', label='Total Touchdowns')

    # Customize the chart
    plt.title('Total Touchdowns Per Season for Derrick Henry', fontsize=16)
    plt.xlabel('Season', fontsize=12)
    plt.ylabel('Total Touchdowns', fontsize=12)
    plt.xticks(rotation=45)  # Rotate season labels for better readability
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Show the line graph
    plt.tight_layout()

    plot_file_path = f"saved_graphs/{playername}.png"
    plt.savefig(plot_file_path)

    aws.upload_file(f"saved_graphs/{playername}.png", "nflfootballwebsite", f"{playername}.png")

    return plot_file_path 


