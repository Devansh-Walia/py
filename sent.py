from flask import Flask, request, jsonify
from transformers import pipeline
from googletrans import Translator
from langdetect import detect

app = Flask(__name__)

# Function for Romanized Hinglish to English Transliteration
def romanized_hinglish_to_english(text):
    translator = Translator()
    english_text = translator.translate(text, src='hi', dest='en').text
    return english_text

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        # Get the input data from the request
        data = request.json
        print(data, "######")
        reviews = data.get('reviews', [])
        id = data.get('id', "")
        print(reviews)

        # Check if the language is already English
        english_reviews = []
        for review in reviews:
            print(review)
            if detect(review) == 'en':
                # If the language is already English, use the review as is
                english_reviews.append(review)
                print("english")
            else:
                # Transliterate Hinglish reviews to English
                print("hinglish")
                english_reviews.append(romanized_hinglish_to_english(review))
        
        print(english_reviews)

        # Perform sentiment analysis using the transformers library
        sentiment_analyzer = pipeline('sentiment-analysis')
        results = sentiment_analyzer(english_reviews)

        # Generate a report
        report = {
            'id': id,
            'sentiments': results,
            'overall_sentiment': 'Positive' if all(result['label'] == 'POSITIVE' for result in results) else 'Mixed/Negative',
        }

        return jsonify(r`eport)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)