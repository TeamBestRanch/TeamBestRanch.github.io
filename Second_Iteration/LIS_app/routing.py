from flask import render_template, url_for, flash, redirect
from LIS_app import app, db, bcrypt
from LIS_app.forms import RegistrationForm, LoginForm
from LIS_app.database import User, Restaurant, RatingButton
from flask_login import login_user, current_user, logout_user

# Page Routes
@app.route("/")
@app.route("/home",  methods=['GET', 'POST'])
def Home():
    return render_template("index.html")


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('RestaurantRankings'))
    form = LoginForm()
    if form.validate_on_submit():
        usr = User.query.filter_by(email = form.email.data).first()
        if usr and (form.password.data == usr.password):
            login_user(usr)
            return redirect(url_for('RestaurantRankings'))
        else:
            flash('Login Unsuccessful. Please check email & password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('RestaurantRankings'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Encrypts User info
        # hashed_password = bcrypt.generate_password_hash(
        #     form.password.data).decode('utf-8')
        user = User(fname=form.fname.data, lname=form.lname.data,
                    email=form.email.data, password=form.password.data)

        # Adds the new user into the database
        db.session.add(user)
        db.session.commit()

        flash('Your Account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Home'))

@app.route('/RestaurantRankings')
def RestaurantRankings():
    return render_template('rankings.html', title='Restaurant Rankings')

