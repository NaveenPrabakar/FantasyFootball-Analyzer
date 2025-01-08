import google.generativeai as genai
import time
import os
genai.configure(api_key=os.getenv("GEMINI_KEY"))
import json
import pandas as pd
import seaborn as sns



#Training the tune model
base_model = "models/gemini-1.5-flash-001-tuning"




def fine_tune():
    operation = genai.create_tuned_model(
    display_name="RB_analyzer",      # Display name for the tuned model
    source_model=base_model,            # The base model to tune
    epoch_count=20,                     # Number of epochs
    batch_size=8,                       # Batch size for training
    learning_rate=0.001,                # Learning rate for fine-tuning
    training_data=training_data,        # Training data
  )

    for status in operation.wait_bar():
       time.sleep(10)
    
    result = operation.result()
    print(result)

    #Visualize the Loss curve of the tuned model
    result = operation.result()

    snapshots = pd.DataFrame(result.tuning_task.snapshots)

    sns.lineplot(data=snapshots, x = 'epoch', y='mean_loss')

test_data = [
    {
        "text_input": "Player: Joe Mixon, Rushing Yards: 1205, Touchdowns: 13, Fumbles: 3, Yards per Carry: 4.5",
        "expected output": "Performance Grade: A-"
    },
    {
        "text_input": "Player: Christian McCaffrey, Rushing Yards: 1400, Touchdowns: 11, Fumbles: 2, Yards per Carry: 4.8",
        "expected output": "Performance Grade: A"
    },
    {
        "text_input": "Player: David Montgomery, Rushing Yards: 1160, Touchdowns: 8, Fumbles: 2, Yards per Carry: 4.3",
        "expected output": "Performance Grade: B"
    },
    {
        "text_input": "Player: Josh Jacobs, Rushing Yards: 1600, Touchdowns: 14, Fumbles: 3, Yards per Carry: 4.9",
        "expected output": "Performance Grade: A"
    },
    {
        "text_input": "Player: DeAndre Swift, Rushing Yards: 617, Touchdowns: 3, Fumbles: 2, Yards per Carry: 4.0",
        "expected output": "Performance Grade: D"
    },
    {
        "text_input": "Player: Miles Sanders, Rushing Yards: 1075, Touchdowns: 6, Fumbles: 1, Yards per Carry: 4.7",
        "expected output": "Performance Grade: B"
    },
    {
        "text_input": "Player: Tony Pollard, Rushing Yards: 1200, Touchdowns: 9, Fumbles: 1, Yards per Carry: 5.0",
        "expected output": "Performance Grade: B+"
    },
    {
        "text_input": "Player: J.K. Dobbins, Rushing Yards: 900, Touchdowns: 7, Fumbles: 1, Yards per Carry: 5.0",
        "expected output": "Performance Grade: B"
    },
    {
        "text_input": "Player: Kareem Hunt, Rushing Yards: 860, Touchdowns: 8, Fumbles: 3, Yards per Carry: 4.1",
        "expected output": "Performance Grade: C"
    },
    {
        "text_input": "Player: Leonard Fournette, Rushing Yards: 780, Touchdowns: 6, Fumbles: 2, Yards per Carry: 4.0",
        "expected output": "Performance Grade: C"
    },
    {
        "text_input": "Player: Raheem Mostert, Rushing Yards: 1072, Touchdowns: 7, Fumbles: 1, Yards per Carry: 5.4",
        "expected output": "Performance Grade: B+"
    },
    {
        "text_input": "Player: James Robinson, Rushing Yards: 1085, Touchdowns: 6, Fumbles: 2, Yards per Carry: 4.5",
        "expected output": "Performance Grade: B"
    },
    {
        "text_input": "Player: Damien Harris, Rushing Yards: 929, Touchdowns: 14, Fumbles: 3, Yards per Carry: 4.6",
        "expected output": "Performance Grade: B+"
    }
]

#Testing the tune model

tuned_models = []
for i, m in zip(range(5), genai.list_tuned_models()):
  tuned_models.append(m.name)

model = genai.GenerativeModel(model_name=tuned_models[1]) #Load in the tuned model

correct_predictions = 0
total_tests = len(test_data)


for test_case in test_data:
    test_input = test_case["text_input"]
    expected_output = test_case["expected output"]

   
    result = model.generate_content(test_input)
    predicted_output = result.text.strip().split("\n")[0]

    
    if predicted_output == expected_output:
        correct_predictions += 1
        print(f"Test passed for input: {test_input}")
    else:
        print(f"Test failed for input: {test_input}")
        print(f"Expected: {expected_output}, Got: {predicted_output}")


accuracy = (correct_predictions / total_tests) * 100
print(f"Accuracy: {accuracy:.2f}%")



