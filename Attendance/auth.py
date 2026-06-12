# auth.py

from database import get_connection

def register_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users(email, password) VALUES(?, ?)",
            (email, password)
        )
        conn.commit()
        conn.close()
        return True

    except:
        conn.close()
        return False

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    return user