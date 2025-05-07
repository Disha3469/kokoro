# Add to your database creation script
connection = sqlite3.connect("health_tracker.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS diet_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    food_name TEXT NOT NULL,
    calories INTEGER NOT NULL,
    fat REAL,
    carbs REAL,
    protein REAL,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")
connection.commit()
connection.close()

from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Database connection helper
def get_db_connection():
    connection = sqlite3.connect("health_tracker.db")
    connection.row_factory = sqlite3.Row
    return connection

# Route for Diet Tracker Page
@app.route('/diet_tracker', methods=['GET', 'POST'])
def diet_tracker():
    connection = get_db_connection()

    if request.method == 'POST':
        # Get form data
        user_id = 1  # Replace with session-based user ID
        food_name = request.form['food_name']
        calories = request.form['calories']
        fat = request.form.get('fat', 0)
        carbs = request.form.get('carbs', 0)
        protein = request.form.get('protein', 0)

        # Insert into database
        connection.execute("""
            INSERT INTO diet_entries (user_id, food_name, calories, fat, carbs, protein)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, food_name, calories, fat, carbs, protein))
        connection.commit()

    # Fetch today's summary
    today_diet = connection.execute("""
        SELECT food_name, calories, fat, carbs, protein
        FROM diet_entries
        WHERE user_id = 1 AND date = CURRENT_DATE
    """).fetchall()

    # Calculate totals
    total_calories = sum([entry['calories'] for entry in today_diet])
    total_fat = sum([entry['fat'] for entry in today_diet])
    total_carbs = sum([entry['carbs'] for entry in today_diet])
    total_protein = sum([entry['protein'] for entry in today_diet])

    connection.close()

    return render_template('diet_tracker.html',
                           today_diet=today_diet,
                           total_calories=total_calories,
                           total_fat=total_fat,
                           total_carbs=total_carbs,
                           total_protein=total_protein,
                           recommended_calories=2000)  # Replace with user-specific goal

@app.route('/api/notify_calories', methods=['GET'])
def notify_calories():
    connection = get_db_connection()
    result = connection.execute("""
        SELECT SUM(calories) as total_calories
        FROM diet_entries
        WHERE user_id = 1 AND date = CURRENT_DATE
    """).fetchone()
    connection.close()

    total_calories = result['total_calories'] or 0
    recommended_calories = 2000  # Replace with user-specific goal

    if total_calories > recommended_calories:
        return jsonify({
            'status': 'exceeded',
            'message': f'You have exceeded your recommended calorie intake by {total_calories - recommended_calories} calories!'
        })
    else:
        return jsonify({
            'status': 'within_limit',
            'message': 'You are within your recommended calorie intake.'
        })