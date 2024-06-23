from flask import Flask, render_template, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# Example of some CBT content and responses
cbt_exercises = [
    {
        "id": 1,
        "title": "Thought Diary",
        "description": "Record and challenge negative thoughts.",
        "steps": [
            "Identify the negative thought.",
            "Describe the situation.",
            "Identify the emotion.",
            "Challenge the thought.",
            "Replace with a positive thought."
        ]
    },
    {
        "id": 2,
        "title": "Behavioral Activation",
        "description": "Engage in positive activities to improve mood.",
        "steps": [
            "Choose a positive activity.",
            "Plan when to do it.",
            "Do the activity.",
            "Reflect on how it made you feel."
        ]
    }
]

def get_response_from_chatbot(user_input):
    # Placeholder AI chatbot response logic
    responses = [
        "That sounds tough. Have you tried any relaxation techniques?",
        "I'm here to help. Can you tell me more about what's on your mind?",
        "Let's work through this together. What's the first step you can take?"
    ]
    return random.choice(responses)

@app.route('/')
def index():
    return render_template('index.html', exercises=cbt_exercises)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['message']
    response = get_response_from_chatbot(user_input)
    return jsonify({'response': response, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

if __name__ == '__main__':
    app.run(debug=True)
