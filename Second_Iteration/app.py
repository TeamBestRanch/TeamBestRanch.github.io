from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates')
# Database configurations
app.config['SECRET_KEY'] = 'faef9429c2bad94dfadbf9f24276e00f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# User Authentication
bcrypt = Bcrypt(app)

# Database for User, RatingButton, and Restaurant


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    scores = db.relationship('RatingButton', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.fname}','{self.lname}', '{self.email}', '{self.img_file}')"


class Restaurant(db.Model):
    restaurant_id = db.Column(db.Integer, primary_key=True)
    restaurant_name = db.Column(db.String(100), nullable=False)
    ranch_name = db.Column(db.String(100), nullable=False)
    ranch_img = db.Column(
        db.String(20), nullable=False, default='default.jpg')
    avg_score = db.Column(db.Integer, nullable=False)
    scores = db.relationship('RatingButton', backref='rated', lazy=True)

    def __repr__(self):
        return f"Restaurant('{self.restaurant_name}', '{self.ranch_name}', '{self.ranch_img}', '{self.avg_score}')"


class RatingButton(db.Model):
    rate_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey(
        'restaurant.restaurant_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Rating('{self.score}')"


# Page Routes
@app.route("/")
@app.route("/home",  methods=['GET', 'POST'])
def Home():
    return render_template("index.html")


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@LIS.com' and form.password.data == 'ranch':
            flash('You have been logged in!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Please check username & password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Encrypts User info
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, lname=form.lname.data,
                    email=form.email.data, password=hashed_password)

        # Adds the new user into the database
        db.session.add(user)
        db.session.commit()

        flash('Your Account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/RestaurantRankings')
def RestaurantRankings():
    return render_template('rankings.html', title='Restaurant Rankings')


if(__name__) == '__main__':
    app.run(debug=True)
