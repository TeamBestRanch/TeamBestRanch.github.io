import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, jsonify, request
from LIS_app import app, db, bcrypt
from LIS_app.forms import RegistrationForm, LoginForm, newRestaurantForm, UpdateAccountForm
from LIS_app.database import User, Restaurant, RatingButton
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, desc


# Page Routes


@app.route("/")
@app.route("/home",  methods=['GET', 'POST'])
def Home():
    return render_template("index.html")


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('UserPage'))
    form = LoginForm()
    if form.validate_on_submit():
        usr = User.query.filter_by(email=form.email.data).first()
        if usr and (form.password.data == usr.password):
            login_user(usr)
            return redirect(url_for('UserPage'))
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


@app.route('/Restaurants', methods=['POST', 'GET'])
def restaurant_db():
    form = newRestaurantForm()
    if form.validate_on_submit():
        restaurant = Restaurant(restaurant_name=form.restaurant_name.data, ranch_name=form.ranch_name.data,
                                ranch_img=form.image.data, avg_score=form.base_score)

        db.session.add(restaurant)
        db.session.commit()
        return redirect(url_for('restaurant_db'))

    else:
        restaurants = Restaurant.query.order_by(Restaurant.restaurant_name)
        return render_template('restaurantsdb.html', title='Restaurants', form=form, restaurants=restaurants)


@app.route('/process', methods=['POST'])
def process():
    if request.method == "POST":
        restName = request.form['restaurant']
        userName = request.form['user']
        score = request.form['score']
        # print(restName, ' ', userName, ' ', score)
        if userName != 'no-user':
            user = db.session.query(User).filter_by(email=userName).first()
            # user.counterRate = user.counterRate + CounterRate

            restaurant = db.session.query(Restaurant).filter_by(
                restaurant_name=restName).first()
            newScore = RatingButton(
                customer_id=user.user_id, restaurant_id=restaurant.restaurant_id, score=score)

            db.session.add(newScore)
            db.session.commit()

            scores_by_restaurant = RatingButton.query.filter_by(
                restaurant_id=restaurant.restaurant_id).all()
            # print(scores_by_restaurant)
            # print(restaurant.restaurant_id, restaurant.avg_score)

            # Calculate average score
            total = 0
            val = 0
            for t in scores_by_restaurant:
                total += 1
                val += t.score

            avg = round(val/total, 2)
            # print(avg)

            restaurant.avg_score = avg
            # RatingCount = RatingCount + 1
            # user.counterRate = RatingCount
            db.session.commit()

            # TO DELETE ALL VALUES IN RATINGBUTTON DB:
            # db.session.query(RatingButton).delete()
            # db.session.commit()

            return jsonify({'avg': avg})
    return jsonify(({'error': 'Invalid user'}))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('Home'))


@app.route('/RestaurantRankings')
def RestaurantRankings():
    restaurants = Restaurant.query.order_by(Restaurant.restaurant_name)
    return render_template('rankings.html', title='Restaurant Rankings', restaurants=restaurants)


def SaveProfPic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/ProfilePhoto', picture_fn)

    output_size = (400, 400)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/UserPage', methods=['POST', 'GET'])
def UserPage():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = SaveProfPic(form.picture.data)
            current_user.img_file = picture_file
        current_user.email = form.email.data
        current_user.AboutUser = form.aboutyou.data
        current_user.HobbyUser = form.hobby.data
        current_user.FavFood = form.FavFood.data
        db.session.commit()
        flash('Your Account has been updated!', 'success')
        return redirect(url_for('UserPage'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.aboutyou.data = current_user.AboutUser
        form.hobby.data = current_user.HobbyUser
    img_file = url_for('static', filename='ProfilePhoto/' +
                       current_user.img_file)
    return render_template('userpage.html', title='User Page', img_file=img_file, form=form)


@ app.route('/TierList', methods=['POST', 'GET'])
def TierList():
    if request.method == "POST":
        # CounterRate = request.form['UserCounter']
        userName = request.form['user']

        if userName != 'no-user':
            user = db.session.query(User).filter_by(email=userName).first()
            user.counterRate = user.counterRate + 1
            db.session.commit()
    user = User.query.order_by(desc(User.counterRate)).all()

    return render_template('tierlist.html', title='Tiers', userList=user)
