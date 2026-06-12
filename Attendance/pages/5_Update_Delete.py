# pages/5_Update_Delete.py

import streamlit as st
from database import get_connection

st.title("Update / Delete Attendance")

conn = get_connection()
cursor = conn.cursor()

records = cursor.execute("""
SELECT
attendance_id,
student_name,
date,
status
FROM attendance
""").fetchall()

if len(records) == 0:

    st.warning("No records available")

else:

    record_map = {
        f"{r[0]} - {r[1]} - {r[2]}": r[0]
        for r in records
    }

    selected_record = st.selectbox(
        "Select Record",
        list(record_map.keys())
    )

    attendance_id = record_map[selected_record]

    record = cursor.execute("""
    SELECT *
    FROM attendance
    WHERE attendance_id=?
    """, (
        attendance_id,
    )).fetchone()

    course = st.text_input(
        "Course",
        value=record[3]
    )

    section = st.text_input(
        "Section",
        value=record[4]
    )

    date_value = st.text_input(
        "Date",
        value=record[5]
    )

    status = st.selectbox(
        "Status",
        ["Present", "Absent", "Late", "Excused"]
    )

    if st.button("Update Record"):

        if (
            course == "" or
            section == "" or
            date_value == ""
        ):

            st.error("Fields cannot be empty")

        else:

            cursor.execute("""
            UPDATE attendance
            SET
            course=?,
            section=?,
            date=?,
            status=?
            WHERE attendance_id=?
            """, (
                course,
                section,
                date_value,
                status,
                attendance_id
            ))

            conn.commit()

            st.success("Attendance Updated Successfully")

    confirm = st.checkbox("Confirm Delete")

    if st.button("Delete Record"):

        if confirm:

            cursor.execute("""
            DELETE FROM attendance
            WHERE attendance_id=?
            """, (
                attendance_id,
            ))

            conn.commit()

            st.success("Record Deleted Successfully")

        else:

            st.warning("Please confirm delete")