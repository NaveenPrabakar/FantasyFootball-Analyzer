import google.generativeai as genai
import time
import os
import json
import pandas as pd
import seaborn as sns

# Configure API Key for Gemini AI
genai.configure(api_key=os.getenv("GEMINI_KEY"))

# Base model to fine-tune
base_model = "models/gemini-1.5-flash-001-tuning"

# Define function to fine-tune the model
def fine_tune():
    operation = genai.create_tuned_model(
        display_name="TE_analyzer",      # Display name for the tuned model
        source_model=base_model,         # Base model to fine-tune
        epoch_count=20,                   # Number of training epochs
        batch_size=8,                      # Batch size
        learning_rate=0.001,               # Learning rate
        training_data=training_data,       # Training dataset
    )

    for status in operation.wait_bar():
       time.sleep(10)
    
    result = operation.result()
    print(result)

    # Visualize the Loss curve of the tuned model
    snapshots = pd.DataFrame(result.tuning_task.snapshots)
    sns.lineplot(data=snapshots, x='epoch', y='mean_loss')

# Define TE training dataset (Sample data)
training_data = [
    {
        "text_input": "Player: Travis Kelce, Receiving Yards: 1338, Touchdowns: 12, Receptions: 105, Yards per Catch: 12.7, Targets: 150, Fumbles: 1",
        "expected_output": "Performance Grade: A+"
    },
    {
        "text_input": "Player: Mark Andrews, Receiving Yards: 1100, Touchdowns: 9, Receptions: 88, Yards per Catch: 12.5, Targets: 120, Fumbles: 1",
        "expected_output": "Performance Grade: A"
    },
    {
        "text_input": "Player: George Kittle, Receiving Yards: 1015, Touchdowns: 8, Receptions: 80, Yards per Catch: 12.7, Targets: 110, Fumbles: 2",
        "expected_output": "Performance Grade: A-"
    },
    {
        "text_input": "Player: Dallas Goedert, Receiving Yards: 830, Touchdowns: 6, Receptions: 72, Yards per Catch: 11.5, Targets: 100, Fumbles: 2",
        "expected_output": "Performance Grade: B+"
    },
    {
        "text_input": "Player: T.J. Hockenson, Receiving Yards: 850, Touchdowns: 5, Receptions: 75, Yards per Catch: 11.3, Targets: 105, Fumbles: 2",
        "expected_output": "Performance Grade: B"
    },
    {
        "text_input": "Player: Darren Waller, Receiving Yards: 790, Touchdowns: 4, Receptions: 70, Yards per Catch: 11.2, Targets: 95, Fumbles: 3",
        "expected_output": "Performance Grade: B-"
    },
    {
        "text_input": "Player: Pat Freiermuth, Receiving Yards: 720, Touchdowns: 4, Receptions: 65, Yards per Catch: 11.1, Targets: 90, Fumbles: 3",
        "expected_output": "Performance Grade: C+"
    },
    {
        "text_input": "Player: Dawson Knox, Receiving Yards: 650, Touchdowns: 4, Receptions: 60, Yards per Catch: 10.8, Targets: 85, Fumbles: 4",
        "expected_output": "Performance Grade: C"
    },
    {
        "text_input": "Player: Mike Gesicki, Receiving Yards: 600, Touchdowns: 3, Receptions: 55, Yards per Catch: 10.9, Targets: 80, Fumbles: 4",
        "expected_output": "Performance Grade: C-"
    },
    {
        "text_input": "Player: Hunter Henry, Receiving Yards: 500, Touchdowns: 2, Receptions: 50, Yards per Catch: 10.0, Targets: 75, Fumbles: 5",
        "expected_output": "Performance Grade: D"
    }
]

# Train the model
fine_tune()

# Test the fine-tuned TE model
tuned_models = []
for i, m in zip(range(5), genai.list_tuned_models()):
    tuned_models.append(m.name)

model = genai.GenerativeModel(model_name=tuned_models[1]) # Load the tuned model

# Define test cases for TE grading
test_data = [
    {
        "text_input": "Player: Evan Engram, Receiving Yards: 750, Touchdowns: 4, Receptions: 70, Yards per Catch: 10.7, Targets: 90, Fumbles: 2",
        "expected_output": "Performance Grade: B-"
    },
    {
        "text_input": "Player: Dalton Schultz, Receiving Yards: 710, Touchdowns: 3, Receptions: 68, Yards per Catch: 10.4, Targets: 85, Fumbles: 2",
        "expected_output": "Performance Grade: C+"
    },
    {
        "text_input": "Player: Gerald Everett, Receiving Yards: 620, Touchdowns: 4, Receptions: 62, Yards per Catch: 10.0, Targets: 80, Fumbles: 3",
        "expected_output": "Performance Grade: C"
    }
]

correct_predictions = 0
total_tests = len(test_data)

for test_case in test_data:
    test_input = test_case["text_input"]
    expected_output = test_case["expected_output"]

    result = model.generate_content(test_input)
    predicted_output = result.text.strip().split("\n")[0]

    if predicted_output == expected_output:
        correct_predictions += 1
        print(f"✅ Test passed for input: {test_input}")
    else:
        print(f"❌ Test failed for input: {test_input}")
        print(f"Expected: {expected_output}, Got: {predicted_output}")

# Print final accuracy
accuracy = (correct_predictions / total_tests) * 100
print(f"\n🎯 Accuracy: {accuracy:.2f}%")
