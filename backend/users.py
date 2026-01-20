from .client import get_client

supabase = get_client()

def get_users():
    return supabase.table("users").select("id, email, role, store").execute().data

def get_user_by_email(email):
    return supabase.table("users").select("*").eq("email", email).single().execute().data
