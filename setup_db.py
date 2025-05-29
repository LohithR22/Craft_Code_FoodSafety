import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('auditing.db')
cursor = conn.cursor()

# Create a table for storing issues
cursor.execute('''CREATE TABLE IF NOT EXISTS issues (
                    id INTEGER PRIMARY KEY,
                    issue_type TEXT,
                    image BLOB,
                    description TEXT
                 )''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
