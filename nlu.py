from transformers import pipeline

class NLU:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

    def analyze_sentiment(self, text):
        result = self.classifier(text)[0]
        return result['label'], result['score']

    def extract_keywords(self, text):
        # Implement keyword extraction here
        # For simplicity, we'll just return the most common words
        words = text.lower().split()
        return list(set([word for word in words if len(word) > 3]))[:5]
