cursor.execute("""
CREATE TABLE IF NOT EXISTS physical_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    steps INTEGER,
    exercise_minutes INTEGER,
    date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
""")
connection.commit()

@app.route('/physical_tracker', methods=['GET', 'POST'])
def physical_tracker():
    connection = get_db_connection()

    if request.method == 'POST':
        user_id = 1  # Replace with session user ID
        steps = request.form['steps_walked']
        exercise_minutes = request.form['exercise_minutes']

        # Insert into database
        connection.execute("""
            INSERT INTO physical_activities (user_id, steps, exercise_minutes)
            VALUES (?, ?, ?)
        """, (user_id, steps, exercise_minutes))
        connection.commit()

    # Fetch today's summary
    today_activity = connection.execute("""
        SELECT steps, exercise_minutes
        FROM physical_activities
        WHERE user_id = 1 AND date = CURRENT_DATE
    """).fetchone()

    connection.close()

    return render_template('physical_tracker.html', today_activity=today_activity or {'steps': 0, 'exercise_minutes': 0})