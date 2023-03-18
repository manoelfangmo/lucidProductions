from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html');

@app.route('/events')
def events():
    return render_template('events.html');

@app.route('/account/createAccount')
def createAccount():
    return render_template('createAccount.html');

@app.route('/account/login')
def login():
    return render_template('login.html');

@app.route('/collaborations')
def collaborations():
    return render_template('collaborations.html');

@app.route('/about')
def about():
    return render_template('about.html');
@app.route('/events/reviews')
def reviews():
    return render_template('reviews.html');

if __name__ == '__main__':
    app.run()
