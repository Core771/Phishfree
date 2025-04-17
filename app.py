from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
from urllib.parse import urlparse
import re
from flask_cors import CORS

# Allow cross-origin requests
app = Flask(__name__, template_folder='website', static_folder='static')
CORS(app)


app = Flask(__name__, template_folder='website', static_folder='static')

model = joblib.load("phishing_detection_model.pkl")

# --- Feature functions ---
def has_ip_address(url):
    return 1 if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url) else 0

def is_shortened(url):
    shortening_services = r"(bit\.ly|tinyurl\.com|goo\.gl|ow\.ly|t\.co)"
    return 1 if re.search(shortening_services, url) else 0

def has_suspicious_keywords(url):
    suspicious_keywords = ['secure', 'account', 'update', 'login', 'verify', 'banking', 'confirm']
    return 1 if any(keyword in url.lower() for keyword in suspicious_keywords) else 0
 
# --- Updated Feature Extraction with Names ---
def extract_features_with_names(url):
    if not url or not isinstance(url, str):
        raise ValueError("Invalid URL format")
    parsed = urlparse(url)
    hostname = parsed.hostname if parsed.hostname is not None else ""

    features = {
        'length_url': len(url),
        'nb_dots': url.count('.'),
        'nb_hyphens': url.count('-'),
        'nb_at': url.count('@'),
        'nb_slashes': url.count('/'),
        'has_https': 1 if 'https' in url.lower() else 0,
        'has_ip': has_ip_address(url),
        'is_shortened': is_shortened(url),
        'suspicious_keywords': has_suspicious_keywords(url),
        'digit_ratio': sum(c.isdigit() for c in url) / len(url),
        'hostname_length': len(hostname)
    }

    feature_array = np.array(list(features.values())).reshape(1, -1)
    return feature_array, features

# --- Flask Routes ---
@app.route('/classify', methods=['POST'])
def classify():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400

        features_array, feature_dict = extract_features_with_names(url)
        prediction = model.predict(features_array)[0]
        result = "Phishing" if prediction == 1 else "Legitimate"

        # Reasoning: identify suspicious features that likely triggered classification
        reasons = []
        if result == "Phishing":
            if feature_dict['has_ip']:
                reasons.append("Uses an IP address instead of a domain name")
            if feature_dict['is_shortened']:
                reasons.append("Uses a URL shortening service")
            if feature_dict['suspicious_keywords']:
                reasons.append("Contains suspicious keywords")
            if feature_dict['nb_at'] > 0:
                reasons.append("Contains '@' symbol")
            if feature_dict['digit_ratio'] > 0.3:
                reasons.append("High ratio of digits in the URL")
            if feature_dict['nb_dots'] > 5:
                reasons.append("Too many dots in the URL")
            if feature_dict['nb_hyphens'] > 4:
                reasons.append("Too many hyphens in the URL")
        else:
            reasons.append("No major phishing patterns detected")

        return jsonify({'url': url, 'result': result, 'reasons': reasons})

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
