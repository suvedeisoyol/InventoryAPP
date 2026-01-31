import streamlit as st
from backend.products import get_products, fetch_products_with_variants
from utils.layout import page_header
from utils.supabase_helpers import get_distinct_values
from utils.auth import current_user

user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")

page_header("📦 Products Lookup")


departments= ["HAIR", "WIG", "CHEMICAL", "GENERAL"] 

# Create 3 equal-width columns
col1, col2, col3 = st.columns(3)

with col1:
    department = st.selectbox("Department", [""] + departments)
    department = department or None
    
    categories = get_distinct_values("products", "category", filters={"department": department})

with col2:
    category = st.selectbox("Category", [""] + categories)
    category = category or None

    brands = get_distinct_values("products", "brand", filters={"department": department, "category": category})
with col3:
    brand = st.selectbox("Select Brand", [""] + brands )
    brand = brand or None

fetched_data = fetch_products_with_variants(department = department, category = category, brand = brand )

st.dataframe(fetched_data)

