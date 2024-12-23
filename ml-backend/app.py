from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

import websearch




app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# TheSportsDB API configurations
API_KEY = "3"  # Free User API Key
BASE_URL = "https://www.thesportsdb.com/api/v1/json"

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Sports Stats Backend"}


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
    


#Grabs a more detailed description of the player that was searched
@app.get("/player/details/{player_id}")
def get_player_details(player_id: str):
    try:
        
        response = requests.get(f"{BASE_URL}/{API_KEY}/playerstats.php?", params={"id": player_id})
        
        if response.status_code == 200:
            data = response.json()
            player_details = data.get("players", [])
            
            
            if not player_details:
                return {"message": f"No details found for player ID '{player_id}'"}
            
            return {"player_details": player_details[0]}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to fetch data. Status code: {response.status_code}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching player details: {e}")





