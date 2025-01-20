from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pymongo import MongoClient
import os
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse, FileResponse
import qb
import aws
import google.generativeai as genai
import rb
from PIL import Image
import requests


# Configure generative AI
genai.configure(api_key= os.getenv("GEMINI_KEY"))

# Initialize FastAPI app
app = FastAPI()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['data_analysis']
collection = db['nfl_files']

# External API Configuration
API_KEY = "3"
BASE_URL = "https://www.thesportsdb.com/api/v1/json"

#QB Class
class QB:
    def __init__(self, player_name: str):
        self.player_name = player_name

    def get_player_stats(self):
        """
        Fetch player statistics by player name from an external API.
        """
        try:
            response = requests.get(f"{BASE_URL}/{API_KEY}/searchplayers.php", params={"p": self.player_name})
            if response.status_code == 200:
                data = response.json()
                players = data.get("player", [])
                if not players:
                    return {"message": f"No player found with the name '{self.player_name}'"}

                return {
                    "players": [
                        {
                            "idPlayer": player.get("idPlayer"),
                            "strPlayer": player.get("strPlayer"),
                            "strTeam": player.get("strTeam"),
                            "strPosition": player.get("strPosition"),
                            "dateBorn": player.get("dateBorn"),
                            "strNationality": player.get("strNationality"),
                            "strDescriptionEN": player.get("strDescriptionEN"),
                        }
                        for player in players
                    ]
                }
            else:
                raise HTTPException(status_code=500, detail=f"Failed to fetch data. Status code: {response.status_code}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching player data: {e}")

    def get_player_career(self):
        """
        Fetch career stats for the QB from the database.
        """
        player_data = collection.find_one({'_id': 'nfl_stats'})
        if not player_data:
            raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

        retrieved_df = pd.DataFrame(player_data['data'])
        if retrieved_df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

        important_columns = [
            "Season", "Age", "Team", "Pos", "G", "Cmp", "Att", "Cmp%", "Yds", "TD", "Int", "Rate"
        ]
        retrieved_df = retrieved_df[important_columns]
        retrieved_df = retrieved_df.applymap(lambda x: None if pd.isna(x) else x)

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

    def serve_plot(self):
        """
        Serve QB plots from AWS or generate new ones.
        """
        if (
            aws.check_file_exists("nflfootballwebsite", f"{self.player_name}.png")
            and aws.check_file_exists("nflfootballwebsite", f"{self.player_name}(1).png")
            and aws.check_file_exists("nflfootballwebsite", f"{self.player_name}(2).png")
        ):
            aws.download("nflfootballwebsite", f"{self.player_name}.png")
            aws.download("nflfootballwebsite", f"{self.player_name}(1).png")
            aws.download("nflfootballwebsite", f"{self.player_name}(2).png")

            return {
                "data": [
                    f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{self.player_name}.png",
                    f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{self.player_name}(1).png",
                    f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{self.player_name}(2).png",
                ]
            }

        le = qb.get_data(self.player_name)
        return {"data": [f"https://winter-break-project.onrender.com/serves_plot/{file_path}" for file_path in le]}

    def prompt(self):
        """
        Generate QB analysis using generative AI.
        """
        image_directory = [
            f"saved_graphs/{self.player_name}.png",
            f"saved_graphs/{self.player_name}(1).png",
            f"saved_graphs/{self.player_name}(2).png",
        ]
        prompt = (
            "You are a professional QB Analyzer specializing in evaluating quarterbacks' performance "
            "through advanced statistical analysis and visualizations. I have a graph that contains key "
            "metrics of a quarterback's performance (e.g., passing yards, completion rate, touchdown-to-interception ratio, pocket presence). "
            "Your task is to:\n"
            "1. Analyze the graph in-depth and extract actionable insights.\n"
            "2. Highlight the quarterback's strengths and weaknesses based on the data presented.\n"
            "3. Identify any patterns, anomalies, or trends that might be critical for improving their game.\n"
            "4. Summarize your analysis in a concise and structured way that can help coaches, analysts, or fans understand the player's performance."
        )
        answers = []
        for image_path in image_directory:
            img = Image.open(image_path)
            response = genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt, img])
            answers.append(response.text)
        return answers

    def ai_analysis(self):
        """
        Generate AI-based QB grade reports.
        """
        tuned_models = []
        for i, m in zip(range(5), genai.list_tuned_models()):
            tuned_models.append(m.name)

        model = genai.GenerativeModel(model_name=tuned_models[0])

        player_data = collection.find_one({'_id': 'nfl_stats'})
        retrieved_df = pd.DataFrame(player_data['data']).applymap(lambda x: None if pd.isna(x) else x)

        records = retrieved_df.to_dict(orient="records")
        converted_data = [
            {
                "text_input": f"Player: {self.player_name}, Passing Yards: {entry['Yds']}, Touchdowns: {entry['TD']}, "
                              f"Interceptions: {entry['Int']}, Completion Percentage: {entry['Cmp%']}%"
            }
            for entry in records
        ]

        fin = [model.generate_content(qb["text_input"]).text.strip().split("\n")[0] for qb in converted_data]
        return fin

    #Todo: Use the model
    def mlforqb(self):
        next_season_data = pd.DataFrame({'Age': [next_age], 'G': [None], 'GS': [None], 'Cmp': [None], 'Att': [None],  'Cmp%': [None], 'TD%': [None],  'Int': [None],  'Int%': [None],  '1D': [None],  
    'Succ%': [None],  'Lng': [None],  'Y/A': [None], 'AY/A': [None],  'Y/C': [None],  'Y/G': [None],  'Rate': [None],  'QBR': [None],  'Sk': [None],  'Yds.1': [None],  'Sk%': [None], 
    'NY/A': [None],  'ANY/A': [None], '4QC': [None],  'GWD': [None],  'AV': [None],  })

        


class RB:
    print()
    #Implement

    def serve_plot(self):
        """
        Serve RB plots from AWS or generate new ones.
        """
        if (
            aws.check_file_exists("nflfootballwebsite", f"{self.player_name}.png")
            and aws.check_file_exists("nflfootballwebsite", f"{self.player_name}(1).png")
            and aws.check_file_exists("nflfootballwebsite", f"{self.player_name}(2).png")
        ):
            aws.download("nflfootballwebsite", f"{self.player_name}.png")
            aws.download("nflfootballwebsite", f"{self.player_name}(1).png")
            aws.download("nflfootballwebsite", f"{self.player_name}(2).png")

            return {
                "data": [
                    f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{self.player_name}.png",
                    f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{self.player_name}(1).png",
                    f"https://winter-break-project.onrender.com/serves_plot/saved_graphs/{self.player_name}(2).png",
                ]
            }

        le = rb.get_data(self.player_name)
        return {"data": [f"https://winter-break-project.onrender.com/serves_plot/{file_path}" for file_path in le]}

class WR:
    print()
    #Implement 

class TE:
    print()
    #Implement


# Routes
@app.get("/")
def root():
    return {"message": "Welcome to the Sports Stat Backend"}

@app.get("/player-stats/{player_name}")
def get_player_stats(player_name: str):
    qb_instance = QB(player_name)
    return qb_instance.get_player_stats()

@app.get("/player/career/{player_name}")
def get_player_career(player_name: str):
    qb_instance = QB(player_name)
    return qb_instance.get_player_career()

@app.get("/serve_plot/{player_name}")
def serve_plot(player_name: str):
    qb_instance = QB(player_name)
    return qb_instance.serve_plot()

@app.get("/analyze/{player_name}")
def analyze_player(player_name: str):
    qb_instance = QB(player_name)
    return qb_instance.prompt()

@app.get("/AI/{playername}")
def ai_analysis(playername: str):
    qb_instance = QB(playername)
    return qb_instance.ai_analysis()

@app.get("/serves_plot/{filename:path}")
def serve_image(filename: str):

    file_path = filename  
    
    
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type='image/png')



@app.get("/search/{playername}")
def search_player_highlights(playername: str):
    connection = aws.connect_to_rds_mysql()

    try:
    
        player_videos = aws.get_player_videos(connection, playername)

        
        if player_videos and len(player_videos) > 0:
            return player_videos[0]["video"]
        else:
            
            youtube_search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={playername}%20highlights&type=video&maxResults=1&key={YOUTUBE_API_KEY}"
            response = requests.get(youtube_search_url)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json().get("error", {}).get("message", "Unknown error"),
                )
            
            if response.status_code == 200:
                data = response.json()
            
                if "items" in data and len(data["items"]) > 0:
                    video_id = data["items"][0].get("id", {}).get("videoId", None)
                    
                    
                    if video_id:
                        aws.insert_data(connection, playername, video_id)
                        return video_id
                    else:
                        return {"error": "Video ID not found"}
                else:
                    return {"error": "No videos found"}
            else:
                return {"error": "Failed to fetch data", "status_code": response.status_code, "message": response.text}
    except Exception as e:
    
        raise HTTPException(status_code=500, detail="Internal Server Error")

















    












