class DialogueManager:
    def __init__(self):
        self.context = []

    def update_context(self, user_input, sentiment, keywords):
        self.context.append({
            'user_input': user_input,
            'sentiment': sentiment,
            'keywords': keywords
        })
        if len(self.context) > 5:
            self.context.pop(0)

    def get_context(self):
        return self.context

    def determine_next_action(self):
        # Implement logic to determine the next action based on context
        if not self.context:
            return "greeting"
        
        last_sentiment = self.context[-1]['sentiment']
        if last_sentiment == 'NEGATIVE':
            return "provide_support"
        elif last_sentiment == 'POSITIVE':
            return "encourage"
        else:
            return "ask_more_info"
