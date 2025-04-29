from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import string
import nltk
nltk.data.path.append('/path/to/another/directory')
nltk.download('punkt')

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('vader_lexicon')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag, ne_chunk
from nltk.sentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize sentiment analyzer
sia = SentimentIntensityAnalyzer()

@app.route('/tokenize', methods=['POST'])
def tokenize_text():
    data = request.get_json()
    text = data.get('text', '')
    logging.error("Error in /tokenize: Some error related to tokenize happened.")

    # Tokenize words
    tokens = word_tokenize(text)

    return jsonify({'tokens': tokens})

@app.route('/clean', methods=['POST'])
def clean_text():
    data = request.get_json()
    text = data.get('text', '')

    # Tokenize and remove stopwords + punctuation
    tokens = word_tokenize(text)
    clean_tokens = [
        word for word in tokens
        if word.lower() not in stopwords.words('english')
        and word not in string.punctuation
    ]

    return jsonify({'clean_tokens': clean_tokens})

@app.route('/keywords', methods=['POST'])
def extract_keywords():
    data = request.get_json()
    text = data.get('text', '')

    tokens = word_tokenize(text)
    clean_tokens = [
        word for word in tokens
        if word.lower() not in stopwords.words('english')
        and word not in string.punctuation
    ]

    # Take top keywords (you can customize by frequency, here just showing unique words)
    keywords = list(set(clean_tokens))

    return jsonify({'keywords': keywords})

@app.route('/ner', methods=['POST'])
def named_entity_recognition():
    data = request.get_json()
    text = data.get('text', '')

    # Tokenize the text
    tokens = word_tokenize(text)
    print(f"Tokens: {tokens}")  # Debugging log

    # POS tagging
    tags = pos_tag(tokens)
    print(f"Tags: {tags}")  # Debugging log

    # Named Entity Recognition
    tree = ne_chunk(tags)
    print(f"Tree: {tree}")  # Debugging log

    # Extracting entities
    entities = []
    for subtree in tree:
        if hasattr(subtree, 'label'):
            entity = " ".join([token for token, pos in subtree.leaves()])
            entities.append({'entity': entity, 'type': subtree.label()})

    print(f"Entities: {entities}")  # Debugging log

    return jsonify({'entities': entities})

@app.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    data = request.get_json()
    text = data.get('text', '')

    sentiment_scores = sia.polarity_scores(text)

    return jsonify({'sentiment': sentiment_scores})

@app.route('/')
def home():
    return "Flask NLP server is running."

# if __name__ == '__main__':
#     app.run()
