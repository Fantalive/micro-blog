import os

class Config:

	SECRET_KEY = os.environ.get('') or 'secret_key'

	JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "super-secret"

	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False