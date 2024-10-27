import os
import logging
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from model import TextGenerator
from nlu import NLU
from dialogue_manager import DialogueManager

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
text_gen = TextGenerator()
nlu = NLU()
dm = DialogueManager()

# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.form['message']
        
        # NLU processing
        sentiment, _ = nlu.analyze_sentiment(user_input)
        keywords = nlu.extract_keywords(user_input)
        
        # Update dialogue context
        dm.update_context(user_input, sentiment, keywords)
        
        # Determine next action
        next_action = dm.determine_next_action()
        
        # Generate response
        response = text_gen.generate_text(f"{next_action}: {user_input}", max_length=100)
        
        return jsonify({'message': user_input, 'response': response})
    except Exception as e:
        logger.error(f"Error processing chat: {e}")
        return jsonify({'message': user_input, 'response': "Sorry, something went wrong."})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
