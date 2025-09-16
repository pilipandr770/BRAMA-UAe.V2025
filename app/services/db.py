import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker, DeclarativeBase
from flask import current_app
from ..config import Config

db_engine = None
SessionFactory = None

class Base(DeclarativeBase):
    pass

def init_db(app):
    global db_engine, SessionFactory
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    db_engine = create_engine(uri, pool_pre_ping=True, future=True)
    SessionFactory = scoped_session(sessionmaker(bind=db_engine, autoflush=False, autocommit=False))

    schema = app.config.get("DB_SCHEMA", "public")
    
    # Only set schema for PostgreSQL, not SQLite
    if not uri.startswith('sqlite'):
        with db_engine.connect() as conn:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))
            conn.execute(text(f"SET search_path TO {schema}, public;"))
            conn.commit()

    # Імпортуємо моделі після ініт
    from ..models.user import User, Role
    from ..models.content import ContentBlock, GalleryImage
    from ..models.project import Project, Vote
    from ..models.finance import Transaction
    from ..models.meeting import Meeting, MeetingVote, MeetingAgendaItem

    # Створюємо таблиці (без Alembic, простий старт)
    if not uri.startswith('sqlite'):
        Base.metadata.schema = schema
    Base.metadata.create_all(db_engine)

def db_session():
    return SessionFactory()

def bootstrap_admin():
    """Створює початкового адміна з ENV, якщо нема."""
    from ..models.user import User, Role
    session = db_session()
    try:
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_pass = os.getenv("ADMIN_PASSWORD")
        if not admin_email or not admin_pass:
            return
        admin = session.query(User).filter(User.email == admin_email).one_or_none()
        if admin is None:
            admin = User(email=admin_email, first_name="Admin", last_name="User")
            admin.set_password(admin_pass)
            # ролі
            for r in ["member", "admin", "founder"]:
                role = session.query(Role).filter(Role.name == r).one_or_none()
                if not role:
                    role = Role(name=r)
                    session.add(role)
            session.add(admin)
            session.flush()
            # призначити адмін/фоундер
            admin_role = session.query(Role).filter(Role.name == "admin").one()
            founder_role = session.query(Role).filter(Role.name == "founder").one()
            admin.roles.extend([admin_role, founder_role])
            session.commit()
    finally:
        session.close()