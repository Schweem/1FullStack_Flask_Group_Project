from datetime import datetime

import pandas as pd
import sqlite3
import requests
import json

from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'this_is_so_secret'  # Change this to a more secure key in a real application
# Configure session to use filesystem

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_KEY_PREFIX'] = 'login_session:'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

# Global variable to store DataFrame
df = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        con = sqlite3.connect('SarasotaBikeGang.db')
        cur = con.cursor()
        cur.execute("SELECT * from users WHERE username=? AND password=?",
                    (request.form['username'], request.form['password']))

        if cur.fetchone() is None:
            con.close()
            return render_template('index.html', message='Invalid credentials', is_authenticated=is_authenticated)
        else:
            # For now, we're not checking the credentials, just setting the session
            con.close()
            session['authenticated'] = True
            session['name'] = request.form['username']
            return redirect(url_for('index'))  # Redirect to the main page after login
    return render_template('index.html', is_authenticated=is_authenticated)

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

def is_authenticated():
    return session.get('authenticated', False)

@app.route('/')
def index():
    global df  # Use the global df variable
    if not is_authenticated():
        return redirect(url_for('login'))

    con = sqlite3.connect('SarasotaBikeGang.db')
    df = pd.read_sql_query("Select station_id, name, status, latitude, longitude from bikeshare_stations", con)
    con.close()
    name = session.get('name', 'Unknown')

    return render_template('availability.html', name=name, stations=df, is_authenticated=is_authenticated)

def bikeAvailability(station_id):
    conn = sqlite3.connect('SarasotaBikeGang.db')
    sql_string = f"SELECT b.bike_id, b.bike_type, b.status_code, s.name, s.status FROM bikes b JOIN bikeshare_stations s ON b.last_station_id = s.station_id WHERE b.last_station_id = {station_id}"

    print(sql_string)
    df = pd.read_sql_query(sql_string, conn)
    conn.close()

    return df


@app.route('/checkAvailability', methods=['POST'])
def check_availability():
    if not is_authenticated():
        return redirect(url_for('login'))

    choice = request.form['location']
    print("what was chosen: ", choice)
    bikes = bikeAvailability(choice)
    print(bikes)

    if bikes.empty:
        return render_template('availability.html', name=session.get('name', 'Unknown'), stations=df, bikes=bikes,
                               message="No bikes available at the selected location", is_authenticated=is_authenticated)

    return render_template('booking.html', name=session.get('name', 'Unknown'), message="Bikes are available",
                           bikes=bikes, is_authenticated=is_authenticated)


@app.route('/bookAndPay', methods=['POST'])
def book_and_pay():
    if not is_authenticated():
        return redirect(url_for('login'))

    # Extract data from the form submission
    bike_id = request.form.get('bike')
    payment_type = request.form.get('paymentType')
    amount = request.form.get('amount')

    # Validate the data (add your own validation logic)

    # Check for missing values
    if not all([bike_id, payment_type, amount]):
        return render_template('payment_error.html', name=session.get('name', 'Unknown'),
                               error_message="Missing values for payment", is_authenticated=is_authenticated)

    # Store payment information in the database
    # You'll need to modify this part based on your database schema
    conn = sqlite3.connect('SarasotaBikeGang.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO payment_history (user_id, trip_index, amount, payment_date, description) VALUES (?, ?, ?, ?, ?)",
                (session.get('user_id'), bike_id, amount, datetime.now(), 'Bike booking payment'))
    conn.commit()
    conn.close()

    # Make the POST request to the payment processing service
    payment_url = 'http://localhost:5000/process_payment'  # Update with your actual URL
    payment_data = {
        "card_number": "1234567890123456",
        "amount": amount,
        "currency": "USD"
    }
    headers = {'Content-type': 'application/json'}
    json_data = json.dumps(payment_data)

    # Make the POST request
    response = requests.post(payment_url, data=json_data, headers=headers)

    # Check the response
    if response.status_code == 200:
        result = response.json()
        print("Payment processed successfully:")
        print(result)
        # Add any additional logic for booking the bike
        return render_template('booking_success.html', name=session.get('name', 'Unknown'), bike_id=bike_id, payment_type=payment_type, amount=amount, is_authenticated=is_authenticated)

    else:
        print("Payment processing failed. Response code:", response.status_code)
        print("Error message:", response.text)
        # Handle payment failure, redirect to an error page or display a message
        return render_template('payment_error.html', name=session.get('name', 'Unknown'), error_message="Payment processing failed", is_authenticated=is_authenticated)

@app.route('/process_payment', methods=['POST'])
def process_payment():
    # Your payment processing logic here
    # This is where you interact with your payment processing service
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)
