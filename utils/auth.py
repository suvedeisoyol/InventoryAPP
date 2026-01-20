import streamlit as st
from backend.users import get_user_by_email

def login(email, password):
    user = get_user_by_email(email)
    if not user:
        return None
    if user["password"] != password:
        return None
    st.session_state["user"] = user
    return user

def logout():
    if "user" in st.session_state:
        del st.session_state["user"]

def current_user():
    return st.session_state.get("user", None)
