from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash




app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///general.db'
db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    image_path = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(300))
    rating = db.Column(db.Float)
    # Define relationships, if any, e.g., reviews
    reviews = db.relationship('Review', backref='restaurant', lazy=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    last_login_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(20), default='user')
    profile_image_url = db.Column(db.String(200))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    bio = db.Column(db.String(200))
        
with app.app_context():
    db.create_all()


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        bio = request.form.get('bio', '')

        new_user = User(username=username, password=password, email=email,
                        first_name=first_name, last_name=last_name, bio=bio)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html')    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/restaurants')
def restaurants():
    all_restaurants = Restaurant.query.all()
    return render_template('restaurants.html', restaurants=all_restaurants)

@app.route('/add-restaurant', methods=['GET', 'POST'])
def addrestaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(
            name=request.form['name'],
            image_path=request.form['image_path'],
            description=request.form['description'],
            rating=float(request.form['rating'])
        )
        db.session.add(new_restaurant)
        db.session.commit()
        return redirect(url_for('restaurants'))
    return render_template('add-restaurant.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # User's credentials are correct
            # Here you would set up the user session
           return redirect(url_for('profile', username=user.username)) # Assuming you have a profile view that uses user_id
        else:
            flash('Invalid email or password')
    return render_template('login.html')
    
@app.route('/profile/<username>')
def profile(username):
    # Your code to display the profile
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)