from flask import Flask, render_template

app = Flask(__name__)



@app.route('/')
def about():
    return render_template('navbar.html');

@app.route('/events')
def events():
    return render_template('events.html');

if __name__ == '__main__':
    app.run()
