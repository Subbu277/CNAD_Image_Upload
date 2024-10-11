import json
import sqlite3
import uuid

# Allow access from multiple threads
db = sqlite3.connect("cnad.db", check_same_thread=False)

def startDb():
    cursor = db.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    create_users_uploads(cursor)
    db.commit()

def create_users_uploads(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_upload'")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute("DROP TABLE user_upload")

    cursor.execute('''CREATE TABLE user_upload (
        id TEXT PRIMARY KEY,
        email TEXT,
        image TEXT,
        transcript TEXT,
        text_path TEXT
    )''')

def add_user_uploads(data):
    user_id = str(uuid.uuid4())
    cursor = db.cursor()
    cursor.execute('''INSERT INTO user_upload (id, email, image, transcript, text_path)
                      VALUES (?, ?, ?, ?, ?)''',
                   (user_id, data['email'], data['image_path'], data['transcript'], data['text_path']))
    db.commit()

def get_records_by_email(email):
    cursor = db.cursor()
    cursor.execute('''SELECT * FROM user_upload WHERE email = ?''', (email,))
    records = cursor.fetchall()

    records_list = []
    for record in records:
        records_list.append({
            'id':record[0],
            'email':record[1],
            'image_path':record[2],
            'transcript':record[3],
            'text_path':record[4]})

    return records_list
