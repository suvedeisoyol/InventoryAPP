from supabase import create_client, Client
import streamlit as st

def get_client() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]  # secure, not exposed in UI
    return create_client(url, key)