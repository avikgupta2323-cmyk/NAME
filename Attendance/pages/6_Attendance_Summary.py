# pages/6_Attendance_Summary.py

import streamlit as st
import pandas as pd
from database import get_connection

st.title("Attendance Summary")

conn = get_connection()

query = """
SELECT
student_id,
student_name,

COUNT(*) AS total_classes,

SUM(
CASE
WHEN status IN ('Present', 'Late')
THEN 1
ELSE 0
END
) AS attended_classes,

SUM(
CASE
WHEN status='Absent'
THEN 1
ELSE 0
END
) AS absences

FROM attendance

GROUP BY student_id, student_name
"""

df = pd.read_sql(query, conn)

if df.empty:

    st.warning("No attendance data available")

else:

    df["attendance_percentage"] = (
        df["attended_classes"] /
        df["total_classes"]
    ) * 100

    df["attendance_percentage"] = (
        df["attendance_percentage"]
        .round(2)
        .astype(str) + "%"
    )

    st.dataframe(
        df,
        use_container_width=True
    )