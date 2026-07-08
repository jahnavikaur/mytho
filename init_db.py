import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    score INTEGER DEFAULT 0
)
''')

# Create questions table
cursor.execute('''
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    answer TEXT
)
''')

conn.commit()
conn.close()

print("Database created successfully!")