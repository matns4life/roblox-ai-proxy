from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        player_message = data.get("message", "")
        personality = data.get("personality", "a friendly character")
        messages = data.get("messages", None)

        # If full conversation history is provided, use it
        if messages and isinstance(messages, list):
            api_messages = messages
        else:
            # Fallback: single message mode
            system_prompt = f"""You are {personality}"""
            api_messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": player_message}
            ]

        # Call OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": api_messages,
                "max_tokens": 150,
                "temperature": 0.9
            }
        )

        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]

        return jsonify({"reply": ai_reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "Hmm, my brain froze for a second. Try again!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
