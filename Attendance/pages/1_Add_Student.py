# pages/1_Add_Student.py

import streamlit as st
from database import get_connection

st.title("Add Student")

conn = get_connection()
cursor = conn.cursor()

student_id = st.text_input("Student ID")
student_name = st.text_input("Student Name")
course = st.text_input("Course")
section = st.text_input("Section")
semester = st.text_input("Semester")

if st.button("Add Student"):

    if (
        student_id == "" or
        student_name == "" or
        course == "" or
        section == "" or
        semester == ""
    ):

        st.error("All fields are required")

    else:

        cursor.execute(
            "SELECT * FROM students WHERE student_id=?",
            (student_id,)
        )

        existing = cursor.fetchone()

        if existing:
            st.error("Duplicate Student ID not allowed")

        else:

            cursor.execute("""
            INSERT INTO students
            VALUES (?, ?, ?, ?, ?)
            """, (
                student_id,
                student_name,
                course,
                section,
                semester
            ))

            conn.commit()

            st.success("Student Added Successfully")

students = cursor.execute(
    "SELECT * FROM students"
).fetchall()

st.subheader("Student List")

st.table(
    students
)