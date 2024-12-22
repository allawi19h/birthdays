from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('birthdays.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # Fetch all birthdays from the database
        conn = get_db_connection()
        birthdays = conn.execute('SELECT * FROM birthdays').fetchall()
        conn.close()
        return render_template('index.html', birthdays=birthdays)

    elif request.method == 'POST':
        # Get the data from the form submission
        name = request.form['name']
        month = request.form['month']
        day = request.form['day']

        # Insert the new birthday into the database
        conn = get_db_connection()
        conn.execute('INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)',
                     (name, month, day))
        conn.commit()
        conn.close()

        # Redirect back to GET to display updated list
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
