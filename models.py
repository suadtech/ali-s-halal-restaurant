from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy() 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'
    
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    bookings = db.relationship('Booking', backref='table', lazy=True)

    def __repr__(self):
        return f'<Table {self.table_number} (Capacity: {self.capacity})>'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    booking_time = db.Column(db.Time, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='confirmed')  # confirmed, cancelled, completed
    special_requests = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)   

    def __repr__(self):
        return f'<Booking {self.id} - Date: {self.booking_date}, Time: {self.booking_time}>'
    
class MenuCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    items = db.relationship('MenuItem', backref='category', lazy=True)
    def __repr__(self):
        return f'<MenuCategory {self.name}>'
    
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_category.id'), nullable=False)

    def __repr__(self):
        return f'<MenuItem {self.name} - ${self.price}>'
    
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  

    def __repr__(self):
        return f'<Contact {self.name} - {self.subject}>'


      
