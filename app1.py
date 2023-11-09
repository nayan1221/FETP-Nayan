pip install flask flask-oauthlib
from flask import Flask, request, redirect, url_for, session
from flask_oauthlib.client import OAuth
import datetime

app = Flask(__name__)
app.secret_key = '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'  # Replace with a secure secret key
oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key='49370556309-a6h4ilikadhlim2193hv11l5ricefqbu.apps.googleusercontent.com',  # Get these from the Google Developer Console
    consumer_secret='YOUR_GOOGLE_CLIENT_SECRET',
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@app.route('/')
def index():
    if 'google_token' in session:
        user_info = google.get('userinfo')
        if user_info.data:
            user_info_data = user_info.data
            user_name = user_info_data.get('name', 'Unknown')
            user_email = user_info_data.get('email', 'Unknown')
            user_picture = user_info_data.get('picture', None)
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            return f'''
            <h1>Welcome, {user_name}!</h1>
            <img src="{user_picture}" alt="Profile Picture">
            <p>Email: {user_email}</p>
            <p>Current Indian Time: {current_time}</p>
            <a href="/logout">Sign Out</a>
            '''

    return '<a href="/login">Login with Google</a>'

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == '__main__':
    app.run()
