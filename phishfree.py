import re
import joblib
import numpy as np
import pandas as pd
from urllib.parse import urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Detect if URL contains an IP address
def has_ip_address(url):
    return 1 if re.match(r'https?://\d+\.\d+\.\d+\.\d+', url) else 0

# Detect URL shortening services
def is_shortened(url):
    shortening_services = r"(bit\.ly|tinyurl\.com|goo\.gl|ow\.ly|t\.co)"
    return 1 if re.search(shortening_services, url) else 0

# Detect suspicious keywords
def has_suspicious_keywords(url):
    suspicious_keywords = ['secure', 'account', 'update', 'login', 'verify', 'banking', 'confirm']
    return 1 if any(keyword in url.lower() for keyword in suspicious_keywords) else 0

# Preprocess dataset and extract features
def preprocess_data(file_path):
    data = pd.read_csv(file_path)
    data['label'] = data['status'].map({'legitimate': 0, 'phishing': 1})

    data['length_url'] = data['url'].apply(len)
    data['nb_dots'] = data['url'].apply(lambda x: x.count('.'))
    data['nb_hyphens'] = data['url'].apply(lambda x: x.count('-'))
    data['nb_at'] = data['url'].apply(lambda x: x.count('@'))
    data['nb_slashes'] = data['url'].apply(lambda x: x.count('/'))
    data['has_https'] = data['url'].apply(lambda x: 1 if 'https' in x.lower() else 0)
    data['has_ip'] = data['url'].apply(has_ip_address)
    data['is_shortened'] = data['url'].apply(is_shortened)
    data['suspicious_keywords'] = data['url'].apply(has_suspicious_keywords)
    data['digit_ratio'] = data['url'].apply(lambda x: sum(c.isdigit() for c in x) / len(x))
    data['hostname_length'] = data['url'].apply(lambda x: len(urlparse(x).hostname) if urlparse(x).hostname else 0)

    feature_columns = [
        'length_url', 'nb_dots', 'nb_hyphens', 'nb_at', 'nb_slashes', 'has_https',
        'has_ip', 'is_shortened', 'suspicious_keywords', 'digit_ratio', 'hostname_length'
    ]

    X = data[feature_columns]
    y = data['label']
    return X, y, feature_columns

# Train model

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "phishing_detection_model.pkl")
    print("✅ Model saved as phishing_detection_model.pkl")

    return model

# Feature extraction for real-time URL
def extract_features_with_names(url):
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
        'hostname_length': len(urlparse(url).hostname) if urlparse(url).hostname else 0
    }
    return np.array(list(features.values())).reshape(1, -1), features

# CLI testing
if __name__ == "__main__":
    dataset_path = "C:/Users/sairu/Downloads/phisfree/phisfree/dataset2.csv"
    X, y, _ = preprocess_data(dataset_path)
    model = train_model(X, y)

    while True:
        test_url = input("Enter a URL to check (or type 'exit' to quit): ").strip()
        if test_url.lower() == 'exit':
            break
        features_array, features_dict = extract_features_with_names(test_url)
        result = "Phishing" if model.predict(features_array)[0] == 1 else "Legitimate"
        print(f"The URL '{test_url}' is classified as: {result}")
        print("\nFeature Contributions:")
        for key, val in features_dict.items():
            print(f" - {key}: {val}")
