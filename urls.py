from flask import Flask
from flask_login import LoginManager
import os
from models import db, User
# Initialize Flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Register blueprints
from urls import main
app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    