# app.py

import streamlit as st
from auth import register_user, login_user
from database import create_tables

create_tables()

st.set_page_config(
    page_title="Student Attendance System",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("Student Attendance Management System")

menu = ["Login", "Register"]

choice = st.sidebar.selectbox("Menu", menu)

if not st.session_state.logged_in:

    if choice == "Register":

        st.subheader("Register")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Register"):

            if email == "" or password == "":
                st.error("All fields are required")

            else:
                success = register_user(email, password)

                if success:
                    st.success("Registration Successful")

                else:
                    st.error("Email already exists")

    elif choice == "Login":

        st.subheader("Login")

        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login_user(email, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.email = email
                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid Credentials")

else:

    st.success(f"Welcome {st.session_state.email}")

    st.write("Use the sidebar to navigate between pages.")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()