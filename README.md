# Flask Chatbot with Weather Integration 🌤️🤖

This is a simple Flask-based chatbot that uses natural language processing with spaCy and integrates live weather data via the OpenWeather API.

## 🔧 Features
- Rule-based intent detection using spaCy
- Real-time weather using OpenWeather API
- Frontend interface with chat history
- Secure API key handling with `.env` file

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/chatbot-weather-flask.git
cd chatbot-weather-flask

## 2. Set up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows


# 3. Install Dependencies
```bash
pip install -r requirements.txt

#4. Create an .env file
Create a file named .env in the root of the project:
OPENWEATHER_API_KEY=your_api_key_here
You can get a free API key from: https://openweathermap.org/api

#5. Run the app
```bash
python app.py
