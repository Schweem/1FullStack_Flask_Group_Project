import pandas as pd

from flask import Flask, render_template, request, session , redirect, url_for
from flask_session import Session
app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Change this to a more secure key in a real application
# Configure session to use filesystem
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'login_session:'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # For now, we're not checking the credentials, just setting the session
        session['authenticated']= True
        session['name'] = request.form['username']
        return redirect(url_for ('index'))  # Redirect to the main page after login
    return render_template('index.html')


@app.route('/logout')
def logout():
    Session.pop('authenticated', None)
    return redirect(url_for('login'))


def is_authenticated():
    return session.get('authenticated', False)

@app.route('/')
def index():
    if not is_authenticated():
        return redirect(url_for('login'))
    # Sample data for demonstration
    data = {
        'station_id': [1, 2, 3],
        'name': ['Station A', 'Station B', 'Station C'],
        'status': ['Active', 'Inactive', 'Active'],
        'latitude': [34.0522, 36.7783, 40.7128],
        'longitude': [-118.2437, -119.4179, -74.0060]
    }
    df = pd.DataFrame(data)

    name=session.get('name', 'Unknown')

    return render_template('availability.html', name=name, stations=df)


def bikeAvailbilty(station_id):
    # Sample data for demonstration
    data = {
        'bike_id': [101, 102, 103],
        'bike_type': ['Mountain', 'Road', 'Hybrid'],
        'last_maintenance_date': ['2023-01-15', '2023-02-10', '2023-03-05'],
        'status_code': [1, 2, 1],
        'comment': ['Good condition', 'Needs tire replacement', 'New bike']
    }

    bikes_df = pd.DataFrame(data)

    return bikes_df


@app.route('/checkAvailability' , methods=['GET', 'POST'])
def checkAvailability():
    choice = request.args.get('station_id')
    print(choice)
    bikes = bikeAvailbilty(choice)
    print (bikes)
    if len (bikes) > 0:
        print("Bike is available")
        return render_template('booking.html', name=session.get('name', 'Unknown'), message="Bikes are available", bikes=bikes)
if __name__ == "__main__":
    app.run(debug=True)
    # print(testvale)
