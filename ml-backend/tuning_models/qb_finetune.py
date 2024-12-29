import google.generativeai as genai
import time
import os
genai.configure(api_key=os.getenv("GEMINI_KEY"))
import json
import pandas as pd
import seaborn as sns



#Training the tune model
base_model = "models/gemini-1.5-flash-001-tuning"

with open('ai_data/training_data.json', 'r') as f:
    training_data = json.load(f)

def fine_tune():
    operation = genai.create_tuned_model(
    display_name="QB_analyzer_v2",      # Display name for the tuned model
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






#Testing the tune model

tuned_models = []
for i, m in zip(range(5), genai.list_tuned_models()):
  tuned_models.append(m.name)


model = genai.GenerativeModel(model_name=tuned_models[0]) #Load in the tuned model

with open('ai_data/test_data.json', 'r') as f:
    test_data = json.load(f)

correct_predictions = 0
total_tests = len(test_data)


for test_case in test_data:
    test_input = test_case["text_input"]
    expected_output = test_case["expected_output"]

   
    result = model.generate_content(test_input)
    predicted_output = result.text.strip()

    
    if predicted_output == expected_output:
        correct_predictions += 1
        print(f"Test passed for input: {test_input}")
    else:
        print(f"Test failed for input: {test_input}")
        print(f"Expected: {expected_output}, Got: {predicted_output}")


accuracy = (correct_predictions / total_tests) * 100
print(f"Accuracy: {accuracy:.2f}%")


