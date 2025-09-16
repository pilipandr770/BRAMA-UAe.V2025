from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from ..forms.member import MemberSurveyForm
from ..forms.project import CreateProjectForm
from ..services.db import db_session
from ..models.project import Project, Vote

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def home():
	session = db_session()
	try:
		projects = session.query(Project).all()
		return render_template("dashboard.html", projects=projects)
	finally:
		session.close()

@dashboard_bp.route("/survey", methods=["GET","POST"])
@login_required
def survey():
	form = MemberSurveyForm()
	if form.validate_on_submit():
		flash("Анкету збережено (демо).","success")
		return redirect(url_for("dashboard.home"))
	return render_template("dashboard.html", form=form)

@dashboard_bp.route("/project/create", methods=["GET","POST"])
@login_required
def create_project():
	form = CreateProjectForm()
	if form.validate_on_submit():
		session = db_session()
		try:
			p = Project(
				author_id=current_user.id,
				title_uk=form.title_uk.data,
				title_de=form.title_de.data,
				desc_uk=form.desc_uk.data,
				desc_de=form.desc_de.data
			)
			session.add(p)
			session.commit()
			flash("Проєкт подано на розгляд.","success")
			return redirect(url_for("dashboard.home"))
		finally:
			session.close()
	return render_template("dashboard.html", form=form)

@dashboard_bp.route("/project/<int:pid>/vote/<int:value>", methods=["POST"])
@login_required
def vote_project(pid, value):
	value = 1 if value>0 else (-1 if value<0 else 0)
	session = db_session()
	try:
		already = session.query(Vote).filter(Vote.project_id==pid, Vote.user_id==current_user.id).one_or_none()
		if already:
			already.value = value
		else:
			v = Vote(project_id=pid, user_id=current_user.id, value=value)
			session.add(v)
		session.commit()
		return ("", 204)
	finally:
		session.close()
