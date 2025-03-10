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
        display_name="WR_analyzer",      # Display name for the tuned model
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

# Define WR training dataset (Sample data)
training_data = [
    {
        "text_input": "Player: Justin Jefferson, Receiving Yards: 1800, Touchdowns: 12, Receptions: 125, Yards per Catch: 14.4, Targets: 160, Fumbles: 1",
        "expected_output": "Performance Grade: A+"
    },
    {
        "text_input": "Player: Tyreek Hill, Receiving Yards: 1720, Touchdowns: 10, Receptions: 119, Yards per Catch: 14.5, Targets: 150, Fumbles: 1",
        "expected_output": "Performance Grade: A"
    },
    {
        "text_input": "Player: CeeDee Lamb, Receiving Yards: 1350, Touchdowns: 8, Receptions: 107, Yards per Catch: 12.6, Targets: 140, Fumbles: 2",
        "expected_output": "Performance Grade: B+"
    },
    {
        "text_input": "Player: Stefon Diggs, Receiving Yards: 1250, Touchdowns: 7, Receptions: 105, Yards per Catch: 11.9, Targets: 135, Fumbles: 2",
        "expected_output": "Performance Grade: B"
    },
    {
        "text_input": "Player: DK Metcalf, Receiving Yards: 1100, Touchdowns: 6, Receptions: 95, Yards per Catch: 11.6, Targets: 130, Fumbles: 3",
        "expected_output": "Performance Grade: B-"
    },
    {
        "text_input": "Player: Chris Godwin, Receiving Yards: 975, Touchdowns: 5, Receptions: 89, Yards per Catch: 10.9, Targets: 120, Fumbles: 3",
        "expected_output": "Performance Grade: C+"
    },
    {
        "text_input": "Player: Michael Pittman Jr., Receiving Yards: 900, Touchdowns: 4, Receptions: 85, Yards per Catch: 10.6, Targets: 110, Fumbles: 2",
        "expected_output": "Performance Grade: C"
    },
    {
        "text_input": "Player: Courtland Sutton, Receiving Yards: 850, Touchdowns: 4, Receptions: 75, Yards per Catch: 11.3, Targets: 100, Fumbles: 3",
        "expected_output": "Performance Grade: C-"
    },
    {
        "text_input": "Player: Jakobi Meyers, Receiving Yards: 750, Touchdowns: 3, Receptions: 70, Yards per Catch: 10.7, Targets: 95, Fumbles: 4",
        "expected_output": "Performance Grade: D+"
    },
    {
        "text_input": "Player: Allen Robinson, Receiving Yards: 650, Touchdowns: 2, Receptions: 60, Yards per Catch: 10.2, Targets: 85, Fumbles: 5",
        "expected_output": "Performance Grade: D"
    }
]

# Train the model
fine_tune()

# Test the fine-tuned WR model
tuned_models = []
for i, m in zip(range(5), genai.list_tuned_models()):
    tuned_models.append(m.name)

model = genai.GenerativeModel(model_name=tuned_models[1]) # Load the tuned model

# Define test cases for WR grading
test_data = [
    {
        "text_input": "Player: Jaylen Waddle, Receiving Yards: 1120, Touchdowns: 6, Receptions: 100, Yards per Catch: 11.2, Targets: 125, Fumbles: 2",
        "expected_output": "Performance Grade: B"
    },
    {
        "text_input": "Player: Terry McLaurin, Receiving Yards: 980, Touchdowns: 5, Receptions: 90, Yards per Catch: 10.9, Targets: 115, Fumbles: 2",
        "expected_output": "Performance Grade: B-"
    },
    {
        "text_input": "Player: Christian Kirk, Receiving Yards: 850, Touchdowns: 4, Receptions: 78, Yards per Catch: 10.9, Targets: 105, Fumbles: 3",
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
