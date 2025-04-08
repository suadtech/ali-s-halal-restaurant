from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from models import db, User, Table, Booking, MenuCategory, MenuItem, Contact
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/menu')
def menu():
    categories = MenuCategory.query.all()
    menu_items = MenuItem.query.filter_by(is_available=True).all()
    return render_template('menu.html', categories=categories, menu_items=menu_items)

# Add more routes here for booking, login, etc.

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    