import os
import logging
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from chatbot_responses import get_response_from_openai

# Example CBT content and responses
cbt_exercises = [
    {
        "id": 1,
        "title": "Anxiety",
        "description": "Rambling, shortness of breath, rapid heartbeat, insomnia. These symptoms can interfere with a person's daily life and may...",
        "image": "anxiety.png"
    },
    {
        "id": 2,
        "title": "Stress",
        "description": "Stress is a natural response to a perceived threat or demand, whether real or imagined. It is a physical and emotional response that...",
        "image": "stress.png"
    },
    {
        "id": 3,
        "title": "Depression",
        "description": "Depression is a mental health condition characterized by persistent feelings of sadness, hopelessness, and a loss of interest...",
        "image": "depression.png"
    }
]

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html', exercises=cbt_exercises)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form['message']
        logger.info(f"User input: {user_input}")
        
        response = get_response_from_openai(user_input)
        logger.info(f"Bot response: {response}")
        
        return jsonify({'response': response, 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return jsonify({'response': 'Sorry, there was an error processing your request.'}), 500

if __name__ == '__main__':
    app.run()
