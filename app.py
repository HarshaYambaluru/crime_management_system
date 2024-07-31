from flask import Flask, render_template, request, redirect
import sqlite3
import base64

app = Flask(__name__)

# Define the SQLite database file
DATABASE = 'crime_management.db'

# Connect to the database
def connect_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create the crimes table if it doesn't exist
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crimes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            photo_data TEXT,
            status TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
create_table()
@app.route('/')
def open():
    return render_template('open.html')
@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/fp')
def fp():
    return render_template('fp.html')
@app.route('/admin')
def admin():
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM crimes')
    crimes = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin.html', crimes=crimes)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Extract data from the form
        description = request.form.get('description')
        location = request.form.get('location')
        photo_data = request.form.get('photo_data')  # Assuming this field is in the form

        # Insert data into the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO crimes (description, location, photo_data, status) VALUES (?, ?, ?, 'Incomplete')",
                       (description, location, photo_data))
        conn.commit()
        conn.close()

        return render_template('reportSuccess.html')

if __name__ == '__main__':
    app.run(debug=True)
