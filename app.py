import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import spacy
import requests

load_dotenv()

nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def detect_intent(doc):
    lemmas = [token.lemma_ for token in doc]

    if any(word in lemmas for word in ["hello", "hi", "hey"]):
        return "greet"
    if any(word in lemmas for word in["bye", "goodbye", "see"]):
        return "goodbye"
    if "time" in lemmas:
        return "ask_time"
    if "weather" in lemmas or "temperature" in lemmas:
        return "ask_weather"
    if any(tok.tag_ == "WRB" for tok in doc):
        return "generic_question"
    
    return "unknown"


def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "https://api.openweathermap.org/data/2.5/weather"


    params = {
        "q" : city,
        "appid" : api_key,
        "units" : "imperial"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The temperature in {city.title()} is {temp}°F with {description}."
        elif response.status_code == 404:
            return f"I couldn't find the weather for '{city}'. Try a different city?"
        else:
            return "Hmm, something went wrong with the weather service."
        
    except Exception as e:
        return f"Error: {e}"

# Chatbot Logic
def get_bot_response(user_input):
    doc = nlp(user_input.lower())
    intent = detect_intent(doc)
    user_input = user_input.lower()


    if intent == "greet":
        return "Hi there! How can I help you?"
    elif intent == "goodbye":
        return "Catch ya later! 👋"
    elif intent == "ask_time":
        return "Current time is: " +  datetime.now().strftime("%I:%M%p")
    elif intent == "ask_weather":
        for ent in doc.ents:
            if ent.label_ == "GPE":
                return get_weather(ent.text)
            return "Sure! What city do you want the weather for?"
    elif intent == "generic_question":
        return "That's a great question — I'll try to learn more about that."
    
    # if named entities are found
    entities = [f"{ent.label_}: {ent.text}" for ent in doc.ents]
    if entities:
        return "I noticed somethhing in your message: " + "; ".join(entities)
    
    return "Hmm, I'm not sure how to respond yet - but I am still learning!"
    

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods = ["POST"])
def chat():
    user_message = request.form["message"]
    bot_response = get_bot_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)