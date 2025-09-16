from flask import Blueprint, request, jsonify, current_app
import requests

api_bp = Blueprint("api", __name__)

@api_bp.route("/chat", methods=["POST"])
def chat():
	"""
	Проксі до OpenAI (сервер зберігає ключ, фронт його не бачить).
	Надсилаємо короткий prompt + історію (спрощено).
	"""
	data = request.get_json(force=True)
	user_msg = data.get("message","").strip()
	if not user_msg:
		return jsonify({"reply":"Порожнє повідомлення."})
	api_key = current_app.config.get("OPENAI_API_KEY","")
	if not api_key:
		return jsonify({"reply":"OpenAI API ключ не налаштовано на сервері."})

	# Демонстраційний запит (Chat Completions)
	try:
		r = requests.post(
			"https://api.openai.com/v1/chat/completions",
			headers={"Authorization": f"Bearer {api_key}"},
			json={
				"model":"gpt-4o-mini",
				"messages":[
					{"role":"system","content":"You are a helpful assistant for a non-profit e.V. website. Answer briefly in Ukrainian."},
					{"role":"user","content": user_msg}
				]
			},
			timeout=30
		)
		r.raise_for_status()
		reply = r.json()["choices"][0]["message"]["content"]
		return jsonify({"reply": reply})
	except Exception as e:
		return jsonify({"reply": f"Помилка звернення до OpenAI: {e}"}), 500
