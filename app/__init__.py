from flask import Flask
from .config import Config
from .services.db import init_db, db_engine, db_session
from .services.i18n import init_babel_like
from flask_login import LoginManager
from .models.user import User
from .routes.public import public_bp
from .routes.auth import auth_bp
from .routes.dashboard import dashboard_bp
from .routes.admin import admin_bp
from .routes.api import api_bp

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
	app = Flask(__name__, static_folder="static", template_folder="templates")
	app.config.from_object(Config)

	# БД, схема, таблиці
	init_db(app)

	# Логін
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		session = db_session()
		try:
			return session.get(User, int(user_id))
		finally:
			session.close()

	# I18N (простий перемикач у сесії)
	init_babel_like(app)

	# Blueprints
	app.register_blueprint(public_bp)
	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
	app.register_blueprint(admin_bp, url_prefix="/admin")
	app.register_blueprint(api_bp, url_prefix="/api")

	return app
