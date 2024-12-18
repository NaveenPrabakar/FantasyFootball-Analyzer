from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from joblib import dump, load
import io

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow communication between frontend and backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Linear regression model
model = None

# Input schema for testing the model
class TestData(BaseModel):
    features: list

# Train model endpoint
@app.post("/train/")
async def train_model(file: UploadFile):
    try:
        # Read the uploaded CSV file
        content = await file.read()
        data = pd.read_csv(io.BytesIO(content))

        # Check if the dataset contains "target" column
        if "target" not in data.columns:
            raise HTTPException(status_code=400, detail="Dataset must have a 'target' column.")

        # Split features and target
        X = data.drop("target", axis=1)
        y = data["target"]

        # Train the Linear Regression model
        global model
        model = LinearRegression()
        model.fit(X, y)

        # Calculate training error
        predictions = model.predict(X)
        mse = mean_squared_error(y, predictions)

        # Save the model
        dump(model, "linear_regression_model.pkl")

        return {"message": "Model trained successfully", "mse": mse}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training model: {e}")

# Test model endpoint
@app.post("/test/")
def test_model(test_data: TestData):
    try:
        # Ensure model is trained
        global model
        if model is None:
            try:
                model = load("linear_regression_model.pkl")
            except:
                raise HTTPException(status_code=400, detail="No trained model found. Train the model first.")

        # Convert input features to numpy array
        features = np.array(test_data.features).reshape(1, -1)
        prediction = model.predict(features)

        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {e}")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the ML Backend"}
