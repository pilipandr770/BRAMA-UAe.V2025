from flask import session, request, g

SUPPORTED_LANGS = ["uk", "de"]

def init_babel_like(app):
	@app.before_request
	def set_lang():
		lang = request.args.get("lang")
		if lang in SUPPORTED_LANGS:
			session["lang"] = lang
		g.lang = session.get("lang", "uk")

def t(g, uk_text, de_text):
	return uk_text if getattr(g, "lang", "uk") == "uk" else de_text
