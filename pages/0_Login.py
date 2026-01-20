import streamlit as st
from utils.auth import login, logout, current_user

st.title("User Authentication")
user = current_user()
if user:
    st.write(f"Welcome, {current_user()['email']}!")
    if st.button("Logout"):
        logout()
        st.success("Logged out successfully")
        st.rerun()


email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user = login(email, password)
    if user:
        st.success("Logged in successfully")
        st.rerun()
    else:
        st.error("Invalid email or password")
