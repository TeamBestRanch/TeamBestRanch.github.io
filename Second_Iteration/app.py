from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'faef9429c2bad94dfadbf9f24276e00f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.fname}','{self.lname}', '{self.email}', '{self.img_file}')"

    # [insert variable name] = db.relationship('[insert class name], backref='', lazy = True) --> To be used to grab info from other tables??
    # db.ForeignKey --> to be used later


@app.route("/")
@app.route("/home",  methods=['GET', 'POST'])
def Home():
    return render_template("index.html")


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@ranch.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Please check username & password!', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(
            f'Account Created for {form.fname.data} {form.lname.data}!', 'success')
        return redirect(url_for('signup'))
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/RestaurantRankings')
def RestaurantRankings():
    return render_template('rankings.html', title='Restaurant Rankings')


if(__name__) == '__main__':
    app.run(debug=True)
