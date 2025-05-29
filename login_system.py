import sqlite3
import hashlib

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check user login
def login_user(username, password):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    conn.close()
    return user

# Function to add new user during signup
def signup_user(username, password, role):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    try:
        cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, hashed_password, role))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists
    conn.close()
    return True

# Function to check if username already exists
def user_exists(username):
    conn = sqlite3.connect('auditing.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    return user
