class DialogueManager:
    def __init__(self):
        self.context = []
        self.current_topic = None

    def update_context(self, user_input, sentiment, keywords):
        self.context.append({
            'user_input': user_input,
            'sentiment': sentiment,
            'keywords': keywords
        })
        if len(self.context) > 10:  # Increased context size for better tracking
            self.context.pop(0)

    def determine_next_action(self):
        if not self.context:
            return "greeting"

        last_interaction = self.context[-1]
        sentiment = last_interaction['sentiment']
        keywords = last_interaction['keywords']

        if 'stress' in keywords or 'anxious' in keywords or 'worried' in keywords:
            self.current_topic = 'stress_management'
            return 'offer_stress_management_techniques'
        elif 'sad' in keywords or 'depressed' in keywords or 'lonely' in keywords:
            self.current_topic = 'mood_improvement'
            return 'offer_mood_improvement_strategies'
        elif sentiment == 'negative':
            return 'provide_emotional_support'
        elif sentiment == 'positive':
            return 'encourage_positive_behavior'
        else:
            return 'ask_open_ended_question'

    def get_context(self):
        return self.context

    def get_current_topic(self):
        return self.current_topic
