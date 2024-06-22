from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model
model = joblib.load('web_phising.model')

# Feature extraction function
def extract_features(url):
    features = {}
    features['url_length'] = len(url)
    features['n_dots'] = url.count('.')
    features['n_hypens'] = url.count('-')
    features['n_underline'] = url.count('_')
    features['n_slash'] = url.count('/')
    features['n_questionmark'] = url.count('?')
    features['n_equal'] = url.count('=')
    features['n_at'] = url.count('@')
    features['n_and'] = url.count('&')
    features['n_exclamation'] = url.count('!')
    features['n_space'] = url.count(' ')
    features['n_tilde'] = url.count('~')
    features['n_comma'] = url.count(',')
    features['n_plus'] = url.count('+')
    features['n_asterisk'] = url.count('*')
    features['n_hastag'] = url.count('#')
    features['n_dollar'] = url.count('$')
    features['n_percent'] = url.count('%')
    features['n_redirection'] = url.count('>')
    return list(features.values())

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get URL from form
        url = request.form['url']
        
        # Extract features from the URL
        features = extract_features(url)
        
        # Make prediction
        prediction = model.predict([features])
        result = 'Phishing' if prediction[0] == 1 else 'Not Phishing'
        
        return render_template('index.html', prediction=result, url=url)

if __name__ == '__main__':
    app.run(debug=True)
