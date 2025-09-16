import os
from dotenv import load_dotenv
load_dotenv()

class Config:
	SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
	SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	DB_SCHEMA = os.getenv("DB_SCHEMA", "public")
	BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
	OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
