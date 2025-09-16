from flask import Blueprint, render_template, g
from ..services.db import db_session
from ..models.content import ContentBlock
from ..services.i18n import t

public_bp = Blueprint("public", __name__)

@public_bp.route("/")
def index():
	session = db_session()
	try:
		blocks = session.query(ContentBlock).all()
		return render_template("index.html", blocks=blocks, t=t, g=g)
	finally:
		session.close()

@public_bp.route("/privacy")
def privacy():
	return render_template("privacy.html")

@public_bp.route("/terms")
def terms():
	return render_template("terms.html")

@public_bp.route("/contacts")
def contacts():
	return render_template("contacts.html")
