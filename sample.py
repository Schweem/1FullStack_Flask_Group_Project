from flask import Flask, request, render_template, session, redirect, url_for,  send_from_directory
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# SQLite database configuration
DATABASE = 'SarasotaBikeGang.db'

# Helper function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Check user credentials and set the session if valid
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else:
            return 'Login failed. Invalid username or password.'

    return render_template('login.html')

# Dashboard route for authenticated users
@app.route('/dashboard')
def dashboard():
    if not session.get('authenticated'):
        return 'Unauthorized', 401

    return 'Welcome to the dashboard!'

# Logout route to clear the session
@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    #returns the static html
    return send_from_directory(".", "index.html")

if __name__ == '__main__':

    app.run(debug=True, port= 5150)
