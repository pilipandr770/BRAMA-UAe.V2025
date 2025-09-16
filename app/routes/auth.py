from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..forms.auth import LoginForm, RegisterForm
from ..services.db import db_session
from ..models.user import User, Role

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("dashboard.home"))
	form = LoginForm()
	if form.validate_on_submit():
		session = db_session()
		try:
			user = session.query(User).filter(User.email==form.email.data).one_or_none()
			if user and user.check_password(form.password.data):
				login_user(user, remember=form.remember.data)
				return redirect(url_for("dashboard.home"))
			flash("Невірний email або пароль","danger")
		finally:
			session.close()
	return render_template("login.html", form=form)

@auth_bp.route("/register", methods=["GET","POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		session = db_session()
		try:
			exist = session.query(User).filter(User.email==form.email.data).one_or_none()
			if exist:
				flash("Користувач із цим email вже існує","warning")
			else:
				u = User(
					email=form.email.data,
					first_name=form.first_name.data,
					last_name=form.last_name.data,
					consent_signed=form.consent.data
				)
				u.set_password(form.password.data)
				# Базова роль — member
				member = session.query(Role).filter(Role.name=="member").one_or_none()
				if not member:
					member = Role(name="member")
					session.add(member)
					session.flush()
				u.roles.append(member)
				session.add(u)
				session.commit()
				login_user(u)
				return redirect(url_for("dashboard.home"))
		finally:
			session.close()
	return render_template("register.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect(url_for("public.index"))
