import os
import nltk

nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Check if punkt and stopwords are already downloaded
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir, quiet=True)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)

from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class NLU:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        # Returns polarity (-1 to 1) and subjectivity (0 to 1)
        polarity = analysis.sentiment.polarity
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        return sentiment, abs(polarity)

    def extract_keywords(self, text):
        word_tokens = word_tokenize(text.lower())
        keywords = [word for word in word_tokens if word.isalnum() and word not in self.stop_words]
        return keywords[:5]  # Return top 5 keywords
