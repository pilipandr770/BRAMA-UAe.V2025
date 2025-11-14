
from flask import Blueprint, render_template, g
from ..services.db import db_session
from ..models.content import ContentBlock
from ..services.i18n import t
from ..models.finance import Transaction
from sqlalchemy.orm import joinedload

public_bp = Blueprint("public", __name__)

@public_bp.route("/finance")
def public_finance():
	session = db_session()
	try:
		# show last 50 transactions, but compute balance across all transactions
		all_txs = session.query(Transaction).all()
		income = sum(tx.amount for tx in all_txs if tx.type == "income")
		expense = sum(tx.amount for tx in all_txs if tx.type == "expense")
		balance = income - expense
		txs = session.query(Transaction).order_by(Transaction.created_at.desc()).limit(50).all()
		return render_template("finance.html", txs=txs, balance=balance, income=income, expense=expense)
	finally:
		session.close()

@public_bp.route("/")
def index():
	session = db_session()
	try:
		# eager-load images so templates can access them after session close
		blocks = session.query(ContentBlock).options(joinedload(ContentBlock.images)).all()
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
