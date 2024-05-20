from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():

	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	jwt.init_app(app)

	from .views.auth import auth_bp
	from .views.blog import blog_bp
	from .views.index import main_bp
	
	app.register_blueprint(auth_bp, url_prefix='/auth')
	app.register_blueprint(blog_bp, url_prefix='/blog')
	app.register_blueprint(main_bp)
	

	return app
