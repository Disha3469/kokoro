from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = sqlite3.connect("health_tracker.db")
    connection.row_factory = sqlite3.Row
    return connection

# Add a new user
@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    age = data.get("age")
    gender = data.get("gender")

    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO users (name, email, age, gender) VALUES (?, ?, ?, ?)",
                       (name, email, age, gender))
        connection.commit()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        connection.close()

# Add health metrics
@app.route("/add_metrics", methods=["POST"])
def add_metrics():
    data = request.json
    user_id = data.get("user_id")
    date = data.get("date")
    steps = data.get("steps")
    calories = data.get("calories")
    heart_rate = data.get("heart_rate")
    sleep_hours = data.get("sleep_hours")

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate, sleep_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, date, steps, calories, heart_rate, sleep_hours))
    connection.commit()
    connection.close()

    return jsonify({"message": "Metrics added successfully"}), 201

# Get user details
@app.route("/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    connection = get_db_connection()
    user = connection.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    connection.close()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    return jsonify(dict(user)), 200

# Get health metrics
@app.route("/get_metrics/<int:user_id>", methods=["GET"])
def get_metrics(user_id):
    connection = get_db_connection()
    metrics = connection.execute("SELECT * FROM health_metrics WHERE user_id = ?", (user_id,)).fetchall()
    connection.close()

    return jsonify([dict(metric) for metric in metrics]), 200

if __name__ == "__main__":
    app.run(debug=True)
