from flask import Blueprint, request, jsonify, current_app
import requests
import json

api_bp = Blueprint("api", __name__)

@api_bp.route("/chat", methods=["POST"])
def chat():
    """OpenAI чат-ендпоїнт для віджета"""
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        openai_key = current_app.config.get("OPENAI_API_KEY")
        if not openai_key:
            return jsonify({"response": "Чат тимчасово недоступний. Chat temporarily unavailable."}), 200
        
        # OpenAI API запит
        headers = {
            "Authorization": f"Bearer {openai_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant for a Ukrainian e.V. (eingetragener Verein) platform. Respond in Ukrainian or German based on user's language. Keep responses concise and helpful."},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            bot_message = result["choices"][0]["message"]["content"]
            return jsonify({"response": bot_message})
        else:
            return jsonify({"response": "Вибачте, виникла помилка. Sorry, an error occurred."}), 200
            
    except Exception as e:
        return jsonify({"response": "Технічна помилка. Technical error."}), 200

@api_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "BRAMA-UAe.V2025"})