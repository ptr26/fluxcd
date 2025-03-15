from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Database connection settings
DB_HOST = 'postgres'  # Use the PostgreSQL service name
DB_NAME = 'guestbook'
DB_USER = 'guestbookuser'
DB_PASSWORD = 'password123'

# Connect to database
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Create table if it doesn't exist
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS guests (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            surname VARCHAR(50),
            length_of_stay INTEGER,
            rating INTEGER
        );
    """)
    conn.commit()
    conn.close()

create_table()

# API endpoint to add guest
@app.route('/add_guest', methods=['POST'])
def add_guest():
    data = request.json
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO guests (name, surname, length_of_stay, rating)
        VALUES (%s, %s, %s, %s);
    """, (data['name'], data['surname'], data['length_of_stay'], data['rating']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Guest added successfully'}), 200

# API endpoint to get all guests
@app.route('/get_guests', methods=['GET'])
def get_guests():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM guests;")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
