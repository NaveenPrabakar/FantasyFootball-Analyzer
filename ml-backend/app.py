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
GEMINI_API_KEY = os.getenv("GEMINI_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_KEY environment variable is not set")
genai.configure(api_key=GEMINI_API_KEY)

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
BACKEND_URL = "https://winter-break-project.onrender.com"

#QB Class
class QB:
    def __init__(self, player_name: str):
        self.player_name = player_name

    def get_player_stats(self):
        """
        Fetch player statistics by player name from an external API.
        """
        try:
            response = requests.get(f"{BASE_URL}/{API_KEY}/searchplayers.php", params={"p": "nfl_stats"})
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
        try:
            player_data = collection.find_one({'_id': 'nfl_stats'})
            if not player_data:
                raise HTTPException(status_code=404, detail="Database not found")

            # Convert the array of objects to a DataFrame
            retrieved_df = pd.DataFrame(player_data['data'])
            if retrieved_df.empty:
                raise HTTPException(status_code=404, detail="No data found in database")

            # Filter for QB position
            qb_df = retrieved_df[retrieved_df['Pos'] == 'QB']
            if qb_df.empty:
                raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found as QB")

            important_columns = [
                "Season", "Age", "Team", "Pos", "G", "Cmp", "Att", "Cmp%", "Yds", "TD", "Int", "Rate"
            ]
            qb_df = qb_df[important_columns]
            qb_df = qb_df.applymap(lambda x: None if pd.isna(x) else x)

            records = qb_df.to_dict(orient="records")
            for record in records:
                for key, value in record.items():
                    if isinstance(value, np.int64):
                        record[key] = int(value)
                    elif isinstance(value, pd.Timestamp):
                        record[key] = value.isoformat()
                    elif isinstance(value, pd.Timedelta):
                        record[key] = value.total_seconds()

            return {"data": records}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching career data: {str(e)}")

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
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}.png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(1).png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(2).png",
                ]
            }

        le = qb.get_data(self.player_name)
        return {"data": [f"{BACKEND_URL}/serves_plot/{file_path}" for file_path in le]}

    def prompt(self):
        """
        Generate QB analysis using generative AI.
        """
        try:
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
            model = genai.GenerativeModel("gemini-pro-vision")
            for image_path in image_directory:
                try:
                    img = Image.open(image_path)
                    response = model.generate_content([prompt, img])
                    answers.append(response.text)
                except Exception as e:
                    answers.append(f"Error analyzing image {image_path}: {str(e)}")
            return answers
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def ai_analysis(self):
        """
        Generate AI-based QB grade reports.
        """
        try:
            model = genai.GenerativeModel("gemini-pro")

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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def mlforqb(self):
        """
        Predict next season's stats for the QB using machine learning.
        """
        try:
            player_data = collection.find_one({'_id': 'nfl_stats'})
            if not player_data:
                raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

            retrieved_df = pd.DataFrame(player_data['data'])
            if retrieved_df.empty:
                raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

            # Get the latest age and increment it for next season
            latest_age = retrieved_df['Age'].max()
            next_age = latest_age + 1

            # Create DataFrame for next season prediction
            next_season_data = pd.DataFrame({
                'Age': [next_age],
                'G': [None], 'GS': [None], 'Cmp': [None], 'Att': [None],
                'Cmp%': [None], 'TD%': [None], 'Int': [None], 'Int%': [None],
                '1D': [None], 'Succ%': [None], 'Lng': [None], 'Y/A': [None],
                'AY/A': [None], 'Y/C': [None], 'Y/G': [None], 'Rate': [None],
                'QBR': [None], 'Sk': [None], 'Yds.1': [None], 'Sk%': [None],
                'NY/A': [None], 'ANY/A': [None], '4QC': [None], 'GWD': [None],
                'AV': [None]
            })

            # TODO: Implement actual ML model prediction here
            # For now, return placeholder data
            return {
                "message": "ML prediction not yet implemented",
                "next_season_data": next_season_data.to_dict(orient='records')[0]
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in ML prediction: {str(e)}")

class RB:
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
        Fetch career stats for the RB from the database.
        """
        player_data = collection.find_one({'_id': 'nfl_stats'})
        if not player_data:
            raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

        retrieved_df = pd.DataFrame(player_data['data'])
        if retrieved_df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

        important_columns = [
            "Season", "Age", "Team", "Pos", "G", "Att", "Yds", "TD", "Y/A", "Lng", "Fmb"
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
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}.png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(1).png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(2).png",
                ]
            }

        le = rb.get_data(self.player_name)
        return {"data": [f"{BACKEND_URL}/serves_plot/{file_path}" for file_path in le]}

    def prompt(self):
        """
        Generate RB analysis using generative AI.
        """
        try:
            image_directory = [
                f"saved_graphs/{self.player_name}.png",
                f"saved_graphs/{self.player_name}(1).png",
                f"saved_graphs/{self.player_name}(2).png",
            ]
            prompt = (
                "You are a professional RB Analyzer specializing in evaluating running backs' performance "
                "through advanced statistical analysis and visualizations. I have a graph that contains key "
                "metrics of a running back's performance (e.g., rushing yards, yards per attempt, touchdowns, fumbles). "
                "Your task is to:\n"
                "1. Analyze the graph in-depth and extract actionable insights.\n"
                "2. Highlight the running back's strengths and weaknesses based on the data presented.\n"
                "3. Identify any patterns, anomalies, or trends that might be critical for improving their game.\n"
                "4. Summarize your analysis in a concise and structured way that can help coaches, analysts, or fans understand the player's performance."
            )
            answers = []
            model = genai.GenerativeModel("gemini-pro-vision")
            for image_path in image_directory:
                try:
                    img = Image.open(image_path)
                    response = model.generate_content([prompt, img])
                    answers.append(response.text)
                except Exception as e:
                    answers.append(f"Error analyzing image {image_path}: {str(e)}")
            return answers
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def ai_analysis(self):
        """
        Generate AI-based RB grade reports.
        """
        try:
            model = genai.GenerativeModel("gemini-pro")

            player_data = collection.find_one({'_id': 'nfl_stats'})
            retrieved_df = pd.DataFrame(player_data['data']).applymap(lambda x: None if pd.isna(x) else x)

            records = retrieved_df.to_dict(orient="records")
            converted_data = [
                {
                    "text_input": f"Player: {self.player_name}, Rushing Yards: {entry['Yds']}, Touchdowns: {entry['TD']}, "
                                  f"Yards per Attempt: {entry['Y/A']}, Fumbles: {entry['Fmb']}"
                }
                for entry in records
            ]

            fin = [model.generate_content(rb["text_input"]).text.strip().split("\n")[0] for rb in converted_data]
            return fin
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def mlforrb(self):
        """
        Predict next season's stats for the RB using machine learning.
        """
        try:
            player_data = collection.find_one({'_id': 'nfl_stats'})
            if not player_data:
                raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

            retrieved_df = pd.DataFrame(player_data['data'])
            if retrieved_df.empty:
                raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

            # Get the latest age and increment it for next season
            latest_age = retrieved_df['Age'].max()
            next_age = latest_age + 1

            # Create DataFrame for next season prediction
            next_season_data = pd.DataFrame({
                'Age': [next_age],
                'G': [None], 'GS': [None], 'Att': [None], 'Yds': [None],
                'TD': [None], 'Y/A': [None], 'Lng': [None], 'Fmb': [None],
                'Y/G': [None], 'R/G': [None], 'Catch%': [None]
            })

            # TODO: Implement actual ML model prediction here
            # For now, return placeholder data
            return {
                "message": "ML prediction not yet implemented",
                "next_season_data": next_season_data.to_dict(orient='records')[0]
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in ML prediction: {str(e)}")

class WR:
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
        Fetch career stats for the WR from the database.
        """
        player_data = collection.find_one({'_id': 'nfl_stats'})
        if not player_data:
            raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

        retrieved_df = pd.DataFrame(player_data['data'])
        if retrieved_df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

        important_columns = [
            "Season", "Age", "Team", "Pos", "G", "Tgt", "Rec", "Yds", "TD", "Y/R", "Lng", "Fmb"
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
        Serve WR plots from AWS or generate new ones.
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
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}.png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(1).png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(2).png",
                ]
            }

        le = wr.get_data(self.player_name)
        return {"data": [f"{BACKEND_URL}/serves_plot/{file_path}" for file_path in le]}

    def prompt(self):
        """
        Generate WR analysis using generative AI.
        """
        try:
            image_directory = [
                f"saved_graphs/{self.player_name}.png",
                f"saved_graphs/{self.player_name}(1).png",
                f"saved_graphs/{self.player_name}(2).png",
            ]
            prompt = (
                "You are a professional WR Analyzer specializing in evaluating wide receivers' performance "
                "through advanced statistical analysis and visualizations. I have a graph that contains key "
                "metrics of a wide receiver's performance (e.g., receptions, receiving yards, touchdowns, yards per catch). "
                "Your task is to:\n"
                "1. Analyze the graph in-depth and extract actionable insights.\n"
                "2. Highlight the wide receiver's strengths and weaknesses based on the data presented.\n"
                "3. Identify any patterns, anomalies, or trends that might be critical for improving their game.\n"
                "4. Summarize your analysis in a concise and structured way that can help coaches, analysts, or fans understand the player's performance."
            )
            answers = []
            model = genai.GenerativeModel("gemini-pro-vision")
            for image_path in image_directory:
                try:
                    img = Image.open(image_path)
                    response = model.generate_content([prompt, img])
                    answers.append(response.text)
                except Exception as e:
                    answers.append(f"Error analyzing image {image_path}: {str(e)}")
            return answers
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def ai_analysis(self):
        """
        Generate AI-based WR grade reports.
        """
        try:
            model = genai.GenerativeModel("gemini-pro")

            player_data = collection.find_one({'_id': 'nfl_stats'})
            retrieved_df = pd.DataFrame(player_data['data']).applymap(lambda x: None if pd.isna(x) else x)

            records = retrieved_df.to_dict(orient="records")
            converted_data = [
                {
                    "text_input": f"Player: {self.player_name}, Receptions: {entry['Rec']}, Receiving Yards: {entry['Yds']}, "
                                  f"Touchdowns: {entry['TD']}, Yards per Reception: {entry['Y/R']}"
                }
                for entry in records
            ]

            fin = [model.generate_content(wr["text_input"]).text.strip().split("\n")[0] for wr in converted_data]
            return fin
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def mlforwr(self):
        """
        Predict next season's stats for the WR using machine learning.
        """
        try:
            player_data = collection.find_one({'_id': 'nfl_stats'})
            if not player_data:
                raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

            retrieved_df = pd.DataFrame(player_data['data'])
            if retrieved_df.empty:
                raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

            # Get the latest age and increment it for next season
            latest_age = retrieved_df['Age'].max()
            next_age = latest_age + 1

            # Create DataFrame for next season prediction
            next_season_data = pd.DataFrame({
                'Age': [next_age],
                'G': [None], 'GS': [None], 'Tgt': [None], 'Rec': [None],
                'Yds': [None], 'TD': [None], 'Y/R': [None], 'Lng': [None],
                'Fmb': [None], 'Y/G': [None], 'R/G': [None], 'Catch%': [None]
            })

            # TODO: Implement actual ML model prediction here
            # For now, return placeholder data
            return {
                "message": "ML prediction not yet implemented",
                "next_season_data": next_season_data.to_dict(orient='records')[0]
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in ML prediction: {str(e)}")

class TE:
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
        Fetch career stats for the TE from the database.
        """
        player_data = collection.find_one({'_id': 'nfl_stats'})
        if not player_data:
            raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

        retrieved_df = pd.DataFrame(player_data['data'])
        if retrieved_df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

        important_columns = [
            "Season", "Age", "Team", "Pos", "G", "Tgt", "Rec", "Yds", "TD", "Y/R", "Lng", "Fmb"
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
        Serve TE plots from AWS or generate new ones.
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
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}.png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(1).png",
                    f"{BACKEND_URL}/serves_plot/saved_graphs/{self.player_name}(2).png",
                ]
            }

        le = te.get_data(self.player_name)
        return {"data": [f"{BACKEND_URL}/serves_plot/{file_path}" for file_path in le]}

    def prompt(self):
        """
        Generate TE analysis using generative AI.
        """
        try:
            image_directory = [
                f"saved_graphs/{self.player_name}.png",
                f"saved_graphs/{self.player_name}(1).png",
                f"saved_graphs/{self.player_name}(2).png",
            ]
            prompt = (
                "You are a professional TE Analyzer specializing in evaluating tight ends' performance "
                "through advanced statistical analysis and visualizations. I have a graph that contains key "
                "metrics of a tight end's performance (e.g., receptions, receiving yards, touchdowns, yards per catch). "
                "Your task is to:\n"
                "1. Analyze the graph in-depth and extract actionable insights.\n"
                "2. Highlight the tight end's strengths and weaknesses based on the data presented.\n"
                "3. Identify any patterns, anomalies, or trends that might be critical for improving their game.\n"
                "4. Summarize your analysis in a concise and structured way that can help coaches, analysts, or fans understand the player's performance."
            )
            answers = []
            model = genai.GenerativeModel("gemini-pro-vision")
            for image_path in image_directory:
                try:
                    img = Image.open(image_path)
                    response = model.generate_content([prompt, img])
                    answers.append(response.text)
                except Exception as e:
                    answers.append(f"Error analyzing image {image_path}: {str(e)}")
            return answers
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def ai_analysis(self):
        """
        Generate AI-based TE grade reports.
        """
        try:
            model = genai.GenerativeModel("gemini-pro")

            player_data = collection.find_one({'_id': 'nfl_stats'})
            retrieved_df = pd.DataFrame(player_data['data']).applymap(lambda x: None if pd.isna(x) else x)

            records = retrieved_df.to_dict(orient="records")
            converted_data = [
                {
                    "text_input": f"Player: {self.player_name}, Receptions: {entry['Rec']}, Receiving Yards: {entry['Yds']}, "
                                  f"Touchdowns: {entry['TD']}, Yards per Reception: {entry['Y/R']}"
                }
                for entry in records
            ]

            fin = [model.generate_content(te["text_input"]).text.strip().split("\n")[0] for te in converted_data]
            return fin
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in AI analysis: {str(e)}")

    def mlforte(self):
        """
        Predict next season's stats for the TE using machine learning.
        """
        try:
            player_data = collection.find_one({'_id': 'nfl_stats'})
            if not player_data:
                raise HTTPException(status_code=404, detail=f"Player '{self.player_name}' not found")

            retrieved_df = pd.DataFrame(player_data['data'])
            if retrieved_df.empty:
                raise HTTPException(status_code=404, detail=f"No data found for player '{self.player_name}'")

            # Get the latest age and increment it for next season
            latest_age = retrieved_df['Age'].max()
            next_age = latest_age + 1

            # Create DataFrame for next season prediction
            next_season_data = pd.DataFrame({
                'Age': [next_age],
                'G': [None], 'GS': [None], 'Tgt': [None], 'Rec': [None],
                'Yds': [None], 'TD': [None], 'Y/R': [None], 'Lng': [None],
                'Fmb': [None], 'Y/G': [None], 'R/G': [None], 'Catch%': [None]
            })

            # TODO: Implement actual ML model prediction here
            # For now, return placeholder data
            return {
                "message": "ML prediction not yet implemented",
                "next_season_data": next_season_data.to_dict(orient='records')[0]
            }

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error in ML prediction: {str(e)}")

# Routes
@app.get("/")
def root():
    return {"message": "Welcome to the Sports Stat Backend"}

@app.get("/player-stats/{player_name}")
def get_player_stats(player_name: str):
    try:
        # Try QB first
        qb_instance = QB(player_name)
        stats = qb_instance.get_player_stats()
        if "message" in stats and "No player found" in stats["message"]:
            # Try RB
            rb_instance = RB(player_name)
            stats = rb_instance.get_player_stats()
            if "message" in stats and "No player found" in stats["message"]:
                # Try WR
                wr_instance = WR(player_name)
                stats = wr_instance.get_player_stats()
                if "message" in stats and "No player found" in stats["message"]:
                    # Try TE
                    te_instance = TE(player_name)
                    stats = te_instance.get_player_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/career/{player_name}")
def get_player_career(player_name: str):
    try:
        # First check if the database exists and has data
        player_data = collection.find_one({'_id': 'nfl_stats'})
        if not player_data:
            raise HTTPException(status_code=404, detail="Database not found")
        
        retrieved_df = pd.DataFrame(player_data['data'])
        if retrieved_df.empty:
            raise HTTPException(status_code=404, detail="No data found in database")

        # Try QB first
        try:
            qb_instance = QB(player_name)
            career = qb_instance.get_player_career()
            return career
        except HTTPException as e:
            if e.status_code == 404:
                # Try RB
                try:
                    rb_instance = RB(player_name)
                    career = rb_instance.get_player_career()
                    return career
                except HTTPException as e:
                    if e.status_code == 404:
                        # Try WR
                        try:
                            wr_instance = WR(player_name)
                            career = wr_instance.get_player_career()
                            return career
                        except HTTPException as e:
                            if e.status_code == 404:
                                # Try TE
                                try:
                                    te_instance = TE(player_name)
                                    career = te_instance.get_player_career()
                                    return career
                                except HTTPException as e:
                                    if e.status_code == 404:
                                        raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found in any position")
                                    raise e
                            raise e
                    raise e
            raise e
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error fetching career data: {str(e)}")

@app.get("/serve_plot/{player_name}")
def serve_plot(player_name: str):
    try:
        # Try QB first
        qb_instance = QB(player_name)
        plots = qb_instance.serve_plot()
        return plots
    except Exception as e:
        try:
            # Try RB
            rb_instance = RB(player_name)
            plots = rb_instance.serve_plot()
            return plots
        except Exception as e:
            try:
                # Try WR
                wr_instance = WR(player_name)
                plots = wr_instance.serve_plot()
                return plots
            except Exception as e:
                try:
                    # Try TE
                    te_instance = TE(player_name)
                    plots = te_instance.serve_plot()
                    return plots
                except Exception as e:
                    raise HTTPException(status_code=404, detail=f"Plots not found for player '{player_name}'")

@app.get("/analyze/{player_name}")
def analyze_player(player_name: str):
    try:
        # Try QB first
        qb_instance = QB(player_name)
        analysis = qb_instance.prompt()
        return analysis
    except Exception as e:
        try:
            # Try RB
            rb_instance = RB(player_name)
            analysis = rb_instance.prompt()
            return analysis
        except Exception as e:
            try:
                # Try WR
                wr_instance = WR(player_name)
                analysis = wr_instance.prompt()
                return analysis
            except Exception as e:
                try:
                    # Try TE
                    te_instance = TE(player_name)
                    analysis = te_instance.prompt()
                    return analysis
                except Exception as e:
                    raise HTTPException(status_code=404, detail=f"Analysis not found for player '{player_name}'")

@app.get("/AI/{playername}")
def ai_analysis(playername: str):
    try:
        # Try QB first
        qb_instance = QB(playername)
        analysis = qb_instance.ai_analysis()
        return analysis
    except Exception as e:
        try:
            # Try RB
            rb_instance = RB(playername)
            analysis = rb_instance.ai_analysis()
            return analysis
        except Exception as e:
            try:
                # Try WR
                wr_instance = WR(playername)
                analysis = wr_instance.ai_analysis()
                return analysis
            except Exception as e:
                try:
                    # Try TE
                    te_instance = TE(playername)
                    analysis = te_instance.ai_analysis()
                    return analysis
                except Exception as e:
                    raise HTTPException(status_code=404, detail=f"AI analysis not found for player '{playername}'")

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

@app.get("/predict/{playername}")
def predict_stats(playername: str):
    """
    Predict next season's stats for a player.
    """
    try:
        # Determine player position and create appropriate instance
        player_data = collection.find_one({'_id': 'nfl_stats'})
        if not player_data:
            raise HTTPException(status_code=404, detail=f"Player '{playername}' not found")

        retrieved_df = pd.DataFrame(player_data['data'])
        if retrieved_df.empty:
            raise HTTPException(status_code=404, detail=f"No data found for player '{playername}'")

        # Get the most recent position
        latest_position = retrieved_df['Pos'].iloc[-1]

        if latest_position == 'QB':
            player_instance = QB(playername)
            return player_instance.mlforqb()
        elif latest_position == 'RB':
            player_instance = RB(playername)
            return player_instance.mlforrb()
        elif latest_position == 'WR':
            player_instance = WR(playername)
            return player_instance.mlforwr()
        elif latest_position == 'TE':
            player_instance = TE(playername)
            return player_instance.mlforte()
        else:
            raise HTTPException(status_code=400, detail=f"Position {latest_position} not supported for predictions")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting stats: {str(e)}")

@app.get("/debug/db")
def debug_db():
    try:
        player_data = collection.find_one({'_id': 'nfl_stats'})
        if not player_data:
            return {"error": "Database not found"}
        
        retrieved_df = pd.DataFrame(player_data['data'])
        if retrieved_df.empty:
            return {"error": "No data found in database"}
        
        # Get unique players and their positions
        players = retrieved_df[['Player', 'Pos']].drop_duplicates()
        return {
            "total_records": len(retrieved_df),
            "unique_players": len(players),
            "sample_players": players.head(10).to_dict(orient='records')
        }
    except Exception as e:
        return {"error": str(e)}

















    












