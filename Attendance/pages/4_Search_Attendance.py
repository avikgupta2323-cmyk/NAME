# pages/4_Search_Attendance.py

import streamlit as st
import pandas as pd
from database import get_connection

st.title("Search Attendance")

conn = get_connection()

student_name = st.text_input("Search by Student Name")
student_id = st.text_input("Search by Student ID")
course = st.text_input("Search by Course")

status = st.selectbox(
    "Attendance Status",
    ["", "Present", "Absent", "Late", "Excused"]
)

query = """
SELECT *
FROM attendance
WHERE 1=1
"""

params = []

if student_name != "":
    query += " AND student_name LIKE ?"
    params.append(f"%{student_name}%")

if student_id != "":
    query += " AND student_id LIKE ?"
    params.append(f"%{student_id}%")

if course != "":
    query += " AND course LIKE ?"
    params.append(f"%{course}%")

if status != "":
    query += " AND status=?"
    params.append(status)

df = pd.read_sql(
    query,
    conn,
    params=params
)

if df.empty:

    st.warning("No matching records found")

else:

    st.dataframe(
        df,
        use_container_width=True
    )