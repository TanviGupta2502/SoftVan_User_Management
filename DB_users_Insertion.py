import sqlite3
import bcrypt

# SQLite database connection
conn = sqlite3.connect('users.db')
cur = conn.cursor()

# Create users table if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                roles TEXT
            )''')
conn.commit()

# Hash passwords
password1 = bcrypt.hashpw(b"password1", bcrypt.gensalt()).decode('utf-8')
password2 = bcrypt.hashpw(b"password2", bcrypt.gensalt()).decode('utf-8')

# Insert users
cur.execute("INSERT INTO users (username, password, roles) VALUES (?, ?, ?)", ("user1", password1, "admin,user"))
cur.execute("INSERT INTO users (username, password, roles) VALUES (?, ?, ?)", ("user2", password2, "user"))
conn.commit()

conn.close()
