from flask import Flask, g
from .config import Config
from .services.db import init_db, db_engine, db_session
from .services.i18n import init_babel_like, t
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
        from sqlalchemy.orm import selectinload
        session = db_session()
        try:
            # Eagerly load the roles to prevent DetachedInstanceError
            user = session.query(User).options(selectinload(User.roles)).filter(User.id == int(user_id)).one_or_none()
            if user:
                # Expunge the user from the session to avoid issues
                session.expunge(user)
            return user
        finally:
            session.close()

    # I18N (простий перемикач у сесії)
    init_babel_like(app)

    # Make t and g globally available in templates
    @app.context_processor
    def inject_template_vars():
        return {'t': t, 'g': g}

    # Blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app