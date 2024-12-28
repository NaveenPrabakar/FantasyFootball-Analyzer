import google.generativeai as genai
import time
import os
genai.configure(api_key=os.getenv("Gemini_key"))



base_model = "models/gemini-1.5-flash-001-tuning"


#Sample data for now
training_data = [
    {
        "text_input": "Player: Patrick Mahomes, Passing Yards: 350, Touchdowns: 3, Interceptions: 0, Completion Percentage: 70%",
        "output": "Performance Grade: A+"
    },
    {
        "text_input": "Player: Tom Brady, Passing Yards: 200, Touchdowns: 1, Interceptions: 2, Completion Percentage: 62%",
        "output": "Performance Grade: B"
    },
    {
        "text_input": "Player: Joe Burrow, Passing Yards: 400, Touchdowns: 4, Interceptions: 1, Completion Percentage: 68%",
        "output": "Performance Grade: A"
    },
    # Add more examples
]


operation = genai.create_tuned_model(
    display_name="QB_analyzer",         # Display name for the tuned model
    source_model=base_model,            # The base model to tune
    epoch_count=20,                     # Number of epochs
    batch_size=2,                       # Batch size for training
    learning_rate=0.001,                # Learning rate for fine-tuning
    training_data=training_data,        # Training data
)

for status in operation.wait_bar():
    time.sleep(10)

result = operation.result()
print(result)


model = genai.GenerativeModel(model_name=result.name)


test_input = "Player: Josh Allen, Passing Yards: 280, Touchdowns: 2, Interceptions: 1, Completion Percentage: 65%"
result = model.generate_content(test_input)

print(result.text)  # Example Output: "Performance Grade: A-"


