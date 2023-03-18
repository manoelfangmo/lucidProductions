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

@app.route('/management')
def management():
    return render_template('management.html');

@app.route('/management/analytics')
def managementAnalytics():
    return render_template('managementanalytics.html');
@app.route('/management/inquiries')
def managementInquiries():
    return render_template('managementinquiries.html');
@app.route('/management/reviews')
def managementReviews():
    return render_template('managementreviews.html');

@app.route('/management/users')
def managementUsers():
    return render_template('managementusers.html');


@app.route('/client')
def client():
    return render_template('client.html');

@app.route('/client/form')
def clientForm():
    return render_template('clientform.html');

@app.route('/guest')
def guest():
    return render_template('guest.html');

@app.route('/guest/flag')
def guestFlag():
    return render_template('guestflag.html');

@app.route('/collaborations/contractWorker')
def contractWorker():
    return render_template('contractWorker.html');

@app.route('/client/interestForm')
def eventInquiry():
    return render_template('eventInquiry.html');

if __name__ == '__main__':
    app.run()
