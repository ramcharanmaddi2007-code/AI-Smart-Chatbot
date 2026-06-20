from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=api_key)

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        print("User message:", user_message)

        chat_history.append({
            "role": "user",
            "content": user_message
        })

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=chat_history,
            temperature=0.7,
            max_tokens=1024
        )

        bot_reply = completion.choices[0].message.content

        chat_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=True)