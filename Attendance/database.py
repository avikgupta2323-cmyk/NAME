# database.py

import os
import sqlite3

# store DB next to this file
DB_NAME = os.path.join(os.path.dirname(__file__), "attendance.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    # return rows as dict-like objects
    conn.row_factory = sqlite3.Row
    # enforce foreign key constraints
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY,
        student_name TEXT NOT NULL,
        course TEXT NOT NULL,
        section TEXT NOT NULL,
        semester TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance(
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        course TEXT NOT NULL,
        section TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL
    )
    """)

    # ensure referential integrity: link attendance to students if student_id exists
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_tmp(
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT NOT NULL,
        student_name TEXT NOT NULL,
        course TEXT NOT NULL,
        section TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(student_id)
    )
    """)

    # If attendance table was already present without FK, migrate data
    cursor.execute("PRAGMA table_info(attendance)")
    cols = cursor.fetchall()
    if cols and not any('FOREIGN KEY' in str(c) for c in cols):
        # copy existing data into tmp table and replace
        cursor.execute("INSERT OR IGNORE INTO attendance_tmp(student_id, student_name, course, section, date, status) SELECT student_id, student_name, course, section, date, status FROM attendance")
        cursor.execute("DROP TABLE IF EXISTS attendance")
        cursor.execute("ALTER TABLE attendance_tmp RENAME TO attendance")

    conn.commit()
    conn.close()