
# print("HELLO WORLD")
# Connect to SQLite database.
# Create a database that will hold User data for both login and sign up (Draw out the diagrams)
# Utilize Flask Framework to see if db will work on github pages

from flask import Flask, render_template, url_for

app = Flask(__name__,template_folder='templates')


@app.route("/")
@app.route("/home",  methods=['GET', 'POST'])
def Home():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template('login.html', title='Login')


@app.route('/signup')
def signup():
    return render_template('signup.html', title='Sign Up')

@app.route('/RestaurantRankings')
def RestaurantRankings():
    return render_template('rankings.html', title='Restaurant Rankings')


if(__name__) == '__main__':
    app.run(debug=True)
