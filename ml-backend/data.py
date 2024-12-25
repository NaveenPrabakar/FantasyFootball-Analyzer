from pymongo import MongoClient
import os


#Connect to MongoDB and the correct connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['data_analysis']
collection = db['nfl_files']


#Save player data to mongoDB
def save_to_mongo(df):
    data_dict = df.to_dict(orient='list')  

    collection.replace_one(
    {'_id': 'nfl_stats'},  
    {'_id': 'nfl_stats', 'data': data_dict},
    upsert=True
)


#Next, get the code from colab



