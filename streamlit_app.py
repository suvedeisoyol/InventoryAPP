import streamlit as st
from utils.auth import current_user
user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")

st.set_page_config(page_title="Inventory System", layout="centered")

st.title("🏪 Inventory Management System")
st.write("Use the sidebar to add products or variants.")

# st.title("User Authentication")
# user = current_user()
# if user:
# st.write(f"Welcome, {current_user()['email']}!")
# if st.button("Logout"):
#     logout()
#     st.success("Logged out successfully")
#     st.rerun()


# email = st.text_input("Email")
# password = st.text_input("Password", type="password")

# if st.button("Login"):
# user = login(email, password)
# if user:
#     st.success("Logged in successfully")
#     st.rerun()
# else:
#     st.error("Invalid email or password")
