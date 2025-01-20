import os
import aws

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from pymongo import MongoClient

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_squared_error


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

    plot_file_path = f"saved_graphs/{playername}.png"
    plt.savefig(plot_file_path)

    aws.upload_file(f"saved_graphs/{playername}.png", "nflfootballwebsite", f"{playername}.png")

    return plot_file_path


def bar(filtered_data, playername):

   
    # Calculate TD% and INT%
    filtered_data['TD%'] = (filtered_data['TD'] / filtered_data['Att']) * 100
    filtered_data['Int%'] = (filtered_data['Int'] / filtered_data['Att']) * 100



    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(filtered_data['Season']))

    # Plotting TD%
    td_bars = plt.bar(index, filtered_data['TD%'], bar_width, label='TD%', color='skyblue')

    # Plotting Int%
    int_bars = plt.bar([i + bar_width for i in index], filtered_data['Int%'], bar_width, label='Int%', color='salmon')


    # Add labels on top of each bar
    for bar in td_bars + int_bars:
       yval = bar.get_height()
       plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')


    plt.xlabel('Season')
    plt.ylabel('Percentage')
    plt.title('TD% vs. Int%')
    plt.xticks([i + bar_width / 2 for i in index], filtered_data['Season'])
    plt.legend()
    plt.tight_layout()

    plot_file_path = f"saved_graphs/{playername}(1).png"
    plt.savefig(plot_file_path)

    aws.upload_file(f"saved_graphs/{playername}(1).png", "nflfootballwebsite", f"{playername}(1).png")

    return plot_file_path


def last(playername, global_df):


    plt.figure(figsize=(10, 6))
    plt.scatter(global_df['Yds'], global_df['QBR'], marker='o', s=100, c='skyblue', edgecolors='black')  # Adjust marker size and color

    # Customize the plot
    plt.title('QBR vs. Passing Yards per Season (Excluding 2017)', fontsize=16)
    plt.xlabel('Passing Yards (Yds)', fontsize=12)
    plt.ylabel('QBR', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Add labels for each point (season)
    for i, txt in enumerate(global_df['Season']):
        plt.annotate(txt, (global_df['Yds'][i], global_df['QBR'][i]), textcoords="offset points", xytext=(5,5), ha='left')

    
    plot_file_path = f"saved_graphs/{playername}(2).png"
    plt.savefig(plot_file_path)

    aws.upload_file(f"saved_graphs/{playername}(2).png", "nflfootballwebsite", f"{playername}(2).png")

    return plot_file_path



def qb_ml(playername, df):
    
    imputer = SimpleImputer(strategy='mean')
    df = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)
    df['Cmp/Att'] = df['Cmp'] / df['Att']  # Completion efficiency
    df['Yds/Att'] = df['Yds'] / df['Att']  # Yard per attempt
    df['Yds/Cmp'] = df['Yds'] / df['Cmp']  # Yard per completion
    df['TD/Att'] = df['TD'] / df['Att']  # Touchdowns per attempt
    df['TD/Cmp'] = df['TD'] / df['Cmp']  # Touchdowns per completion
    
    # Scale the features
    scaler = StandardScaler()
    df_scaled = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    
    # Select features (we can keep all numerical columns)
    features = ['Age', 'G', 'GS', 'Cmp', 'Att', 'Cmp%', 'Int', 'Int%', '1D', 'Succ%', 'Lng', 
            'Y/A', 'AY/A', 'Y/C', 'Y/G', 'Rate', 'QBR', 'Sk', 'Yds.1', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD', 'AV',
            'Cmp/Att', 'Yds/Att', 'Yds/Cmp', 'TD/Att', 'TD/Cmp']
            
    X = df_scaled[features]
    y_yds = df_scaled['Yds']
    
    # Hyperparameter tuning for Ridge, Lasso, and ElasticNet
    
    ridge_model = Ridge()
    lasso_model = Lasso()
    elasticnet_model = ElasticNet()
    
    # Hyperparameter grids for tuning
    
    param_grid = {
        'Ridge': {'alpha': [0.01, 0.1, 1, 10, 100]},
        'Lasso': {'alpha': [0.01, 0.1, 1, 10, 100]},
        'ElasticNet': {'alpha': [0.01, 0.1, 1, 10, 100], 'l1_ratio': [0.1, 0.5, 0.9]}
        }
        
    best_models = {}
    
    for model_name, model in zip(['Ridge', 'Lasso', 'ElasticNet'], [ridge_model, lasso_model, elasticnet_model]):
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid[model_name], cv=5, n_jobs=-1, scoring='neg_mean_squared_error')
        grid_search.fit(X, y_yds)
        
        best_models[model_name] = grid_search.best_estimator_
        predictions = grid_search.best_estimator_.predict(X)
        mse = mean_squared_error(y_yds, predictions)
        
    best_model_name = min(best_models, key=lambda model: mean_squared_error(y_yds, best_models[model].predict(X)))
    best_model = best_models[best_model_name]
    # Train the best model on the entire dataset
     
    best_model.fit(X, y_yds)




    

    


 













