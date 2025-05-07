import sqlite3
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

# Establish a connection to the SQLite database
connection = sqlite3.connect('health_tracker.db')
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    age INTEGER,
    bmi REAL,
    cholesterol INTEGER,
    blood_pressure INTEGER,
    heart_rate INTEGER,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")
connection.commit()

@app.route('/health_tracker', methods=['GET', 'POST'])
def health_tracker():
    connection = get_db_connection()

    if request.method == 'POST':
        user_id = 1  # Replace with session user ID
        age = request.form['age']
        bmi = request.form['bmi']
        cholesterol = request.form['cholesterol']
        blood_pressure = request.form['blood_pressure']
        heart_rate = request.form['heart_rate']

        # Insert into database
        connection.execute("""
            INSERT INTO health_metrics (user_id, age, bmi, cholesterol, blood_pressure, heart_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, age, bmi, cholesterol, blood_pressure, heart_rate))
        connection.commit()

    # Fetch the latest metrics
    latest_metrics = connection.execute("""
        SELECT age, bmi, cholesterol, blood_pressure, heart_rate
        FROM health_metrics
        WHERE user_id = 1
        ORDER BY date DESC
        LIMIT 1
    """).fetchone()

    connection.close()

    return render_template('health_tracker.html', latest_metrics=latest_metrics)

@app.route('/predict_risk', methods=['POST'])
def predict_risk():
    data = request.json
    age = data.get('age')
    bmi = data.get('bmi')
    cholesterol = data.get('cholesterol')
    blood_pressure = data.get('blood_pressure')
    heart_rate = data.get('heart_rate')

    # Dummy risk calculation (replace with ML model)
    risk = (int(bmi) + int(cholesterol) + int(blood_pressure)) / 10

    return jsonify({
        'risk': round(risk, 2),
        'level': 'High' if risk > 50 else 'Moderate' if risk > 30 else 'Low'
    })