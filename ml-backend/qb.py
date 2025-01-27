import os
import aws

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from pymongo import MongoClient

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
import joblib



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


def retrain_model(data_path='path_to_new_data.csv', save_path='./models/'):

    
    def load_data():
        df = pd.read_csv(data_path)  
        df = df.drop(columns=['Awards', 'Season', 'Team', 'Lg', 'Pos', 'QBrec'])  
        df = df.iloc[:-2]  
        df = df.dropna()  
        return df

    
    def preprocess_data(df):
        features = ['Age', 'G', 'GS', 'Cmp', 'Att', 'Cmp%', 'TD%', 'Int', 'Int%', '1D', 'Succ%', 'Lng',
                    'Y/A', 'AY/A', 'Y/C', 'Y/G', 'Rate', 'QBR', 'Sk', 'Yds.1', 'Sk%', 'NY/A', 'ANY/A', '4QC', 'GWD', 'AV']
        targets = ['Yds', 'TD', 'Int']
        
        X = df[features]
        y = df[targets]
        
        return X, y

    
    def train_model(X_train, y_train):
        model_yds = RandomForestRegressor(n_estimators=100, random_state=42)
        model_tds = RandomForestRegressor(n_estimators=100, random_state=42)
        model_ints = RandomForestRegressor(n_estimators=100, random_state=42)

        model_yds.fit(X_train, y_train['Yds'])
        model_tds.fit(X_train, y_train['TD'])
        model_ints.fit(X_train, y_train['Int'])

        return model_yds, model_tds, model_ints

    
    def evaluate_model(model_yds, model_tds, model_ints, X_test, y_test):
        y_pred_yds = model_yds.predict(X_test)
        y_pred_tds = model_tds.predict(X_test)
        y_pred_ints = model_ints.predict(X_test)

        mae_yds = mean_absolute_error(y_test['Yds'], y_pred_yds)
        mae_tds = mean_absolute_error(y_test['TD'], y_pred_tds)
        mae_ints = mean_absolute_error(y_test['Int'], y_pred_ints)

        r2_yds = r2_score(y_test['Yds'], y_pred_yds)
        r2_tds = r2_score(y_test['TD'], y_pred_tds)
        r2_ints = r2_score(y_test['Int'], y_pred_ints)

        print(f"MAE (Yds): {mae_yds:.2f}, R² (Yds): {r2_yds:.2f}")
        print(f"MAE (TDs): {mae_tds:.2f}, R² (TDs): {r2_tds:.2f}")
        print(f"MAE (Ints): {mae_ints:.2f}, R² (Ints): {r2_ints:.2f}")

   
    df = load_data()  
    X, y = preprocess_data(df)

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
    model_yds, model_tds, model_ints = train_model(X_train, y_train)

    
    evaluate_model(model_yds, model_tds, model_ints, X_test, y_test)

    
    joblib.dump(model_yds, f'{save_path}model_yds.pkl')
    joblib.dump(model_tds, f'{save_path}model_tds.pkl')
    joblib.dump(model_ints, f'{save_path}model_ints.pkl')

    print("Models saved successfully!")





    

    


 













