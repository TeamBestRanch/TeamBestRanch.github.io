from LIS_app import db, login_manager
from flask_login import UserMixin


# Loads the user accounts
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


# Database for User, RatingButton, and Restaurant
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    scores = db.relationship('RatingButton', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.fname}','{self.lname}', '{self.email}', '{self.img_file}')"
    
    # Overrides and gets the No `id` attribute bug
    def get_id(self):
        return (self.user_id)


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