from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection settings
DB_HOST = 'postgres'  # Use the PostgreSQL service name
DB_NAME = 'guestbook'
DB_USER = 'guestbookuser'
DB_PASSWORD = 'password123'

# Connect to database
def connect_db():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

# Create table if it doesn't exist
def create_table():
    conn = None
    try:
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
        logger.info("Table created or already exists")
    except Exception as e:
        logger.error(f"Error creating table: {e}")
        raise
    finally:
        if conn:
            conn.close()

try:
    create_table()
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")

# API endpoint to add guest
@app.route('/add_guest', methods=['POST'])
def add_guest():
    conn = None
    try:
        data = request.json
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO guests (name, surname, length_of_stay, rating)
            VALUES (%s, %s, %s, %s);
        """, (data['name'], data['surname'], data['length_of_stay'], data['rating']))
        conn.commit()
        logger.info(f"Guest added: {data['name']} {data['surname']}")
        return jsonify({'message': 'Guest added successfully'}), 200
    except Exception as e:
        logger.error(f"Error adding guest: {e}")
        return jsonify({'error': 'Failed to add guest'}), 500
    finally:
        if conn:
            conn.close()

# API endpoint to get all guests
@app.route('/get_guests', methods=['GET'])
def get_guests():
    conn = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM guests ORDER BY id DESC;")
        rows = cur.fetchall()
        logger.info(f"Retrieved {len(rows)} guests")
        return jsonify(rows)
    except Exception as e:
        logger.error(f"Error retrieving guests: {e}")
        return jsonify({'error': 'Failed to retrieve guests'}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
