import streamlit as st

def text_input(label, key=None):
    return st.text_input(label, key=key)

def submit_button(label="Submit"):
    return st.form_submit_button(label)
