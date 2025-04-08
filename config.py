import os

# Secret key for session management
SECRET_KEY = os.environ.get('SECRET_KEY', 'ali-halal-restaurant-secret-key')

# Database configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///restaurant.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Restaurant configuration
RESTAURANT_NAME = "Ali's Halal Food Restaurant"
OPENING_HOUR = 10  # 10 AM
CLOSING_HOUR = 22  # 10 PM
MAX_BOOKING_DAYS_AHEAD = 30

