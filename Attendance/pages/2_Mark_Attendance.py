# pages/2_Mark_Attendance.py

import streamlit as st
from database import get_connection
from datetime import date

st.title("Mark Attendance")

conn = get_connection()
cursor = conn.cursor()

students = cursor.execute(
    "SELECT * FROM students"
).fetchall()

if len(students) == 0:

    st.warning("Please add students first")

else:

    student_options = {
        f"{s[0]} - {s[1]}": s
        for s in students
    }

    selected_student = st.selectbox(
        "Select Student",
        list(student_options.keys())
    )

    attendance_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    status = st.selectbox(
        "Attendance Status",
        ["Present", "Absent", "Late", "Excused"]
    )

    if st.button("Save Attendance"):

        student = student_options[selected_student]

        cursor.execute("""
        INSERT INTO attendance(
            student_id,
            student_name,
            course,
            section,
            date,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            student[0],
            student[1],
            student[2],
            student[3],
            str(attendance_date),
            status
        ))

        conn.commit()

        st.success("Attendance Saved Successfully")