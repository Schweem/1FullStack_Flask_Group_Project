import pandas as pd
import sqlite3

from flask import Flask, render_template, request, session , redirect, url_for
from flask_session import Session
app = Flask(__name__)
app.secret_key = 'some_secret_key'  # Change this to a more secure key in a real application
# Configure session to use filesystem

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_KEY_PREFIX'] = 'login_session:'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        con = sqlite3.connect('SarasotaBikeGang.db')
        cur = con.cursor()
        cur.execute("SELECT * from users WHERE username=? AND password=?", (request.form['username'], request.form['password']))

        if cur.fetchone() is None:
            con.close()
            return render_template('index.html', message='Invalid credentials')
        else:
            # For now, we're not checking the credentials, just setting the session
            con.close()
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
    # if not is_authenticated():
    #     return redirect(url_for('login'))
    # Sample data for demonstration
    data = {
        'station_id': [1, 2, 3],
        'name': ['Station A', 'Station B', 'Station C'],
        'status': ['Active', 'Inactive', 'Active'],
        'latitude': [34.0522, 36.7783, 40.7128],
        'longitude': [-118.2437, -119.4179, -74.0060]
    }

    df = pd.DataFrame(data)
    print (df)
    con = sqlite3.connect('SarasotaBikeGang.db')
    df = pd.read_sql_query("Select station_id, name, status, latitude, longitude from bikeshare_stations", con)
    print(df.head())
    con.close()
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
    conn = sqlite3.connect('SarasotaBikeGang.db')
    sqlString = "select b.bike_id, b.bike_type, b.status_code, s.name, s.status from bikes b join bikeshare_stations s on b.last_station_id = s.station_id where b.last_station_id = " + station_id
    print (sqlString)
    df = pd.read_sql_query(sqlString, conn)
    # bikes_df = pd.DataFrame(data)


    return df


@app.route('/checkAvailability' , methods=['GET', 'POST'])
def checkAvailability():
    choice = request.form['location']
    print("what was chosen: " , choice)
    bikes = bikeAvailbilty(choice)
    print (bikes)
    if len (bikes) > 0:
        print("Bike is available")
        return render_template('booking.html', name=session.get('name', 'Unknown'), message="Bikes are available", bikes=bikes)

if __name__ == "__main__":
    app.run(debug=True)
    # print(testvale)
