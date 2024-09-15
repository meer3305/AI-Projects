from flask import Flask, request, jsonify, render_template
import datetime

app = Flask(__name__)

# Function to process user input
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Initial greeting
    if "hello" in user_input or "hi" in user_input:
        return "Hello jii! How can I assist you?\nKya chahiye farmaye saab?"
    
    # Add more responses
    elif "how are you" in user_input:
        return "I'm just a bot, but I'm functioning as expected. How about you?"
    elif "your name" in user_input:
        return "I'm your Chatty your friendly chat bot! Always here to help you."
    elif "tell me secrect" in user_input:
        return "I am programmed by Meer"
    elif "your age" in user_input:
        return "I am 1 year old"
    elif "kya karre" in user_input:
        return "Tumhein yaad kar raha tha :("
    elif "thank you" in user_input or "thanks" in user_input:
        return "You're welcome! Let me know if you need anything else."
    elif "bye" in user_input:
        return "Goodbye! Have a great day!"
    elif "help" in user_input:
        return "Sure, I can assist you. Please ask your question."
    elif "weather" in user_input:
        return "The weather is sunny, perfect for a walk!"
    elif "yo" in user_input:
        return "Yo! What's up?"
    elif "what is your name" in user_input:
        return "My name is Chatty, nice to meet you."
    elif "time" in user_input:
        return f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}"
    elif "date" in user_input:
        return f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')}"
    elif "what is your purpose" in user_input:
        return "My purpose is to assist you with any questions or tasks you may have."
    elif "sup" in user_input:
        return "Sup boii! Sojaoo ><"
    else:
        return "I'm not sure how to respond to that. Can you ask something else?"

# Welcome page route
@app.route("/")
def welcome():
    return render_template("welcome.html")

# Chatbot page route
@app.route("/chat")
def chat():
    return render_template("index.html")

# Chatbot response route
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json["user_input"]
    response = chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
