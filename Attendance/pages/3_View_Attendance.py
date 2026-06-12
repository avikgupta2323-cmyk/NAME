# pages/3_View_Attendance.py

import streamlit as st
import pandas as pd
from database import get_connection

st.title("View Attendance Records")

conn = get_connection()

query = """
SELECT
attendance_id,
student_id,
student_name,
course,
section,
date,
status
FROM attendance
"""

df = pd.read_sql(query, conn)

if df.empty:

    st.warning("No attendance records available")

else:

    st.dataframe(
        df,
        use_container_width=True
    )