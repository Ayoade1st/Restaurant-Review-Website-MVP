from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)  # Make sure this line is present

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)  # Store password hashes, not plain text
    email = db.Column(db.String(254), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')
    profile_image_url = db.Column(db.Text)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.Text)

    reviews = db.relationship('Review', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Restaurant(db.Model):
    __tablename__ = 'Restaurant'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    email = db.Column(db.String(254))
    website_url = db.Column(db.Text)
    cuisine_type = db.Column(db.String(50))
    operating_hours = db.Column(db.Text)
    rating_average = db.Column(db.DECIMAL(3, 2))
    review_count = db.Column(db.Integer, default=0)
    menu = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    owner = db.relationship('User', backref='restaurants', lazy=True)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)
    ratings = db.relationship('Rating', backref='restaurant', lazy=True)

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class Review(db.Model):
    __tablename__ = 'Review'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('Restaurant.id'), nullable=False)
    rating = db.Column(db.DECIMAL(2, 1), nullable=False)
    title = db.Column(db.String(100))
    review_text = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=db.func.current_timestamp())
    likes = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='approved')
    helpful_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Review {self.id}>'

class Rating(db.Model):
    __tablename__ = 'Rating'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('Restaurant.id'), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    ip_address = db.Column(db.String(45))

    def __repr__(self):
        return f'<Rating {self.id}>'