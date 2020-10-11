from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from app import User NEED TO FIX  CAN'T IMPORT FROM APP RIGHT NOW

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
    
    def validate_field(self, email):
        user = User.query.filter_by(email = email.data).all()
        if user:
            raise ValidationError('Account for email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit_login = SubmitField('Login')
