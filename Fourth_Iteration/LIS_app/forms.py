from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from LIS_app.database import User, Restaurant, UserInfo


class RegistrationForm(FlaskForm):
    fname = StringField('First Name', validators=[
                        DataRequired(), Length(min=2, max=100)])
    lname = StringField('Last Name', validators=[
                        DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_signup = SubmitField('Sign Up')

    # Custom validation for users

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).all()
        if user:
            raise ValidationError('Account for email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit_login = SubmitField('Login')


class newRestaurantForm(FlaskForm):
    restaurant_name = StringField(
        'Restaurant Name', validators=[DataRequired()])
    ranch_name = StringField('Ranch Name', validators=[DataRequired()])
    image = StringField('Image Name', validators=[DataRequired()])
    base_score = int(1)
    submit_restaurant = SubmitField('Add New Restaurant')


class UpdateAccountForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit_signup = SubmitField('Update')
    # Custom validation for users

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).all()
            if user:
                raise ValidationError('Account for email already exists!')