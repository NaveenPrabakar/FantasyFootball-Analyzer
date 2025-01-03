from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pymongo import MongoClient
import os
import pandas as pd
from fastapi.responses import JSONResponse
import numpy as np
from fastapi.responses import FileResponse
import qb
import aws
import google.generativeai as genai


genai.configure(api_key=os.getenv("GEMINI_KEY"))




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

#Mongo DB Collection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['data_analysis']
collection = db['nfl_files']

# TheSportsDB API configurations
API_KEY = "3"  # Free User API Key
BASE_URL = "https://www.thesportsdb.com/api/v1/json"

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Sports Stat Backend"}


#Grabs the basic Info about the player that is searched
@app.get("/player-stats/{player_name}")
def get_player_stats(player_name: str):
    """
    Fetch player statistics by player name from an external API.

    Args:
        player_name (str): Name of the player to search for.

    Returns:
        dict: Player statistics or error message if no player is found.
    """
    try:
        
        response = requests.get(f"{BASE_URL}/{API_KEY}/searchplayers.php", params={"p": player_name})


        
        if response.status_code == 200:
            data = response.json()
            players = data.get("player", [])

            
            if not players:
                return {"message": f"No player found with the name '{player_name}'"}

           
            player_data = []
            for player in players:
                player_data.append({
                    "idPlayer": player.get("idPlayer"),
                    "strPlayer": player.get("strPlayer"),
                    "strTeam": player.get("strTeam"),
                    "strPosition": player.get("strPosition"),
                    "dateBorn": player.get("dateBorn"),
                    "strNationality": player.get("strNationality"),
                    "strDescriptionEN": player.get("strDescriptionEN"),
                })

            
            return {"players": player_data}
        else:
            
            raise HTTPException(status_code=500, detail=f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        
        raise HTTPException(status_code=500, detail=f"Error fetching player data: {e}")
    

#Grabs the actual stats of the player
@app.get("/player/career/{player_name}")
def get_player_career(player_name: str):


    player_data = collection.find_one({'_id': 'nfl_stats'})

    if not player_data:
        raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")

    retrieved_df = pd.DataFrame(player_data['data'])

    if retrieved_df.empty:
        raise HTTPException(status_code=404, detail=f"No data found for player '{player_name}'")


    
    #Replace Nan with None so JSON can handle it
    retrieved_df = retrieved_df.applymap(lambda x: False if pd.isna(x) else x)

    #Import qb stats
    important_columns = [
    "Season",
    "Age",
    "Team",
    "Pos",
    "G",
    "Cmp",
    "Att",
    "Cmp%",
    "Yds",
    "TD",
    "Int",
    "Rate",
    ]

    retrieved_df = retrieved_df[important_columns]

    # Convert the DataFrame to a list of dictionaries
    records = retrieved_df.to_dict(orient="records")

    for record in records:
        for key, value in record.items():
            if isinstance(value, np.int64):
                record[key] = int(value) 
            
            elif isinstance(value, pd.Timestamp):
                record[key] = value.isoformat()  
            elif isinstance(value, pd.Timedelta):
                record[key] = value.total_seconds() 

    return {"data": records}


#stores the images in temp folders, then calls api to retreive them
@app.get("/serve_plot/{player_name}")
def serve_plot(player_name: str):

    if(aws.check_file_exists("nflfootballwebsite", f"{player_name}.png") and aws.check_file_exists("nflfootballwebsite", f"{player_name}(1).png") and 
       aws.check_file_exists("nflfootballwebsite", f"{player_name}(2).png")):
        
        aws.download("nflfootballwebsite", f"{player_name}.png")
        aws.download("nflfootballwebsite", f"{player_name}(1).png")
        aws.download("nflfootballwebsite", f"{player_name}(2).png")

        file_paths = [
            f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{player_name}.png",
            f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{player_name}(1).png",
            f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{player_name}(2).png"
        ]
        
        return {"data": file_paths}

    le = qb.get_data(player_name)
    
    plot_file_urls = [f"https://winter-break-project.onrender.com/serves_plot/{file_path}" for file_path in le]

    return {"data": plot_file_urls}

#Gets the image to the front end
@app.get("/serves_plot/{filename:path}")
def serve_image(filename: str):

    file_path = filename  
    
    
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type='image/png')

#Get a grade report of the player, season by season
@app.get("/AI/{playername}")
def ai_analysis(playername: str):

    tuned_models = []
    for i, m in zip(range(5), genai.list_tuned_models()):
        tuned_models.append(m.name)

    #Use the QB fine tune
    model = genai.GenerativeModel(model_name=tuned_models[0])

    player_data = collection.find_one({'_id': 'nfl_stats'})

    retrieved_df = pd.DataFrame(player_data['data'])

    retrieved_df = retrieved_df.applymap(lambda x: False if pd.isna(x) else x)

    records = retrieved_df.to_dict(orient="records")

    # Convert the JSON data into the desired format
    converted_data = []

    for entry in records:
        player_name = f"Player: {playername}"  # Placeholder for player name, update as needed
        passing_yards = entry["Yds"]
        touchdowns = entry["TD"]
        interceptions = entry["Int"]
        completion_percentage = entry["Cmp%"]
    
        text_input = f"Player: {player_name}, Passing Yards: {passing_yards}, Touchdowns: {touchdowns}, Interceptions: {interceptions}, Completion Percentage: {completion_percentage}%"
        converted_data.append({
            "text_input": text_input
        })

    fin = []

    for qb in converted_data:
        test_input = qb["text_input"] 

        result = model.generate_content(test_input)
        result = result.text.strip()

        fin.append(result)

    cleaned_output = []
    for item in fin:
        # Split by newline to remove commentary, keep only the first line
        cleaned_entry = item.split("\n")[0]
        # Append the cleaned entry
        cleaned_output.append(cleaned_entry)



    return cleaned_output












    












