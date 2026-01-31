import streamlit as st
from backend.products import add_product
from backend.users import get_users
from utils.layout import page_header, divider
from utils.supabase_helpers import get_distinct_values

from utils.auth import current_user
user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")


page_header("➕ Add Product")


departments= ["HAIR", "WIG", "CHEMICAL", "GENERAL"] 
department = st.selectbox("Department", departments)

categories = get_distinct_values("products", "category", filters={"department": department})
category = st.selectbox("Select Category", categories, accept_new_options = True)

brand = st.selectbox("Select Brand", get_distinct_values("products", "brand", filters={"department": department, "category": category}), accept_new_options = True)

subbrand = st.selectbox("Select Subbrand", get_distinct_values("products", "subbrand", filters={"department": department, "category": category, "brand": brand}), accept_new_options = True)

product_name = st.text_input("Product Name")
size = st.text_input("Size")



if st.button("Add Product"):
    
    user_id =user["id"]

    add_product({
        "department": department.upper(),
        "category": category.upper(),
        "product": product_name.upper(),
        "size": size.upper() if size else "",
        "brand": brand.upper(),
        "subbrand": subbrand.upper()  if subbrand else "",
        "created_by": user_id
    })

    st.success(f"Product '{product_name}' added successfully!")
