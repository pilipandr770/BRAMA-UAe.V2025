from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file
from flask_login import login_required
from ..services.security import roles_required
from ..services.db import db_session
from ..models.user import User, Role
from ..models.content import ContentBlock, GalleryImage
from ..models.finance import Transaction
from io import BytesIO

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
@roles_required("admin")
def home():
	session = db_session()
	try:
		users = session.query(User).all()
		blocks = session.query(ContentBlock).all()
		txs = session.query(Transaction).order_by(Transaction.created_at.desc()).limit(20).all()
		return render_template("admin.html", users=users, blocks=blocks, txs=txs)
	finally:
		session.close()

@admin_bp.route("/role", methods=["POST"])
@login_required
@roles_required("admin")
def set_role():
	session = db_session()
	try:
		user_id = int(request.form["user_id"])
		role_name = request.form["role"]
		user = session.get(User, user_id)
		role = session.query(Role).filter(Role.name==role_name).one_or_none()
		if not role:
			role = Role(name=role_name)
			session.add(role)
			session.flush()
		if role not in user.roles:
			user.roles.append(role)
		session.commit()
		flash("Роль призначено.","success")
	finally:
		session.close()
	return redirect(url_for("admin.home"))

@admin_bp.route("/block/create", methods=["POST"])
@login_required
@roles_required("admin")
def create_block():
	session = db_session()
	try:
		block_type = request.form.get("block_type","info")
		b = ContentBlock(
			block_type=block_type,
			title_uk=request.form.get("title_uk",""),
			title_de=request.form.get("title_de",""),
			body_uk=request.form.get("body_uk",""),
			body_de=request.form.get("body_de",""),
		)
		session.add(b)
		session.commit()
		return redirect(url_for("admin.home"))
	finally:
		session.close()

@admin_bp.route("/block/<int:bid>/image", methods=["POST"])
@login_required
@roles_required("admin")
def add_block_image(bid):
	file = request.files.get("image")
	if not file:
		return redirect(url_for("admin.home"))
	session = db_session()
	try:
		img = GalleryImage(
			block_id=bid,
			image_bytes=file.read(),
			caption_uk=request.form.get("caption_uk",""),
			caption_de=request.form.get("caption_de","")
		)
		session.add(img)
		session.commit()
		return redirect(url_for("admin.home"))
	finally:
		session.close()

@admin_bp.route("/image/<int:iid>")
def image_raw(iid):
	session = db_session()
	try:
		img = session.get(GalleryImage, iid)
		if not img:
			return ("",404)
		return send_file(BytesIO(img.image_bytes), mimetype="image/jpeg")
	finally:
		session.close()

@admin_bp.route("/finance/add", methods=["POST"])
@login_required
@roles_required("admin")
def add_finance():
	session = db_session()
	try:
		tx = Transaction(
			type=request.form["type"],
			amount=float(request.form["amount"]),
			currency=request.form.get("currency","EUR"),
			description=request.form.get("description","")
		)
		session.add(tx)
		session.commit()
		return redirect(url_for("admin.home"))
	finally:
		session.close()
