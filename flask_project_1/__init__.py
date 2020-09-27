
from flask import Flask


from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_project_1.config import Config



# USED import secrets 
#secrets.token_hex(16)

db=SQLAlchemy()
bcrypt=Bcrypt()
login_manager=LoginManager()
login_manager.login_view="users.login"

mail = Mail()




def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flask_project_1.users.routes import users
	from flask_project_1.posts.routes import posts
	from flask_project_1.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app

