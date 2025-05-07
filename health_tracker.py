import sqlite3

def create_database():
    connection = sqlite3.connect("health_tracker.db")
    cursor = connection.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER,
        gender TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    # Create health_metrics table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS health_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date DATE NOT NULL,
        steps INTEGER,
        calories INTEGER,
        heart_rate REAL,
        sleep_hours REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    # Create predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        prediction_date DATE NOT NULL,
        predicted_metric TEXT NOT NULL,
        value REAL,
        confidence REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )""")

    connection.commit()
    connection.close()

# Run to create the database
create_database()
