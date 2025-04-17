🔐 PhishFree – Real-Time Phishing Detection Framework
PhishFree is a real-time, machine learning-based phishing detection framework designed for proactive web security. Built using Python and JavaScript, it combines a lightweight Chrome extension with a Flask-powered backend to automatically analyze every URL you visit and assess its legitimacy on the fly.

⚙️ Key Features
Real-Time URL Monitoring: Instantly checks every website you visit in your browser without manual input.

Machine Learning Classification: Uses a trained ML model to distinguish between phishing and legitimate URLs based on multiple heuristics.

Detailed Alerting: Provides browser notifications with specific reasons for why a URL is flagged as suspicious (e.g., shortened URLs, suspicious keywords, and abnormal patterns).

Cross-Origin Communication: Enables secure data exchange between the browser extension and the Flask backend using CORS.

Extendable & Customizable: Easily add new features, detection rules, or integrate with external threat intelligence feeds.

🧠 Detection Features
Identification of URL shortening services (bit.ly, tinyurl, etc.)

Suspicious keywords (e.g., "secure", "login", "account")

Presence of @ symbol and high digit ratio

Excessive use of dots and hyphens

HTTPS usage analysis

🖥️ Tech Stack
Frontend: Chrome Extension (JavaScript, manifest v3)

Backend: Flask (Python), CORS-enabled

Model: Trained with scikit-learn using URL-based feature extraction

Packaging: Easily portable and ready-to-run as a local project with minimal setup

🚀 Use Cases
Personal Browsing Protection

Enterprise Endpoint Security Add-On

Cybersecurity Research & Simulation

Phishing Awareness Training Tools

📦 Installation
📌 Requires: Python 3.8+, Chrome Browser, Flask

Clone the repo and install requirements

Run python app.py to start the Flask server

Load the extension into Chrome via chrome://extensions

Start browsing – and let PhishFree do the rest!

🛡️ Disclaimer
PhishFree is developed for educational, awareness, and research purposes. Always use responsibly and in compliance with applicable laws.

📁 Project Status
🟢 Active – Open to contributions, feedback, and enhancements.
Check out the Issues or submit a PR!
