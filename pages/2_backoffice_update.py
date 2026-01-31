import streamlit as st
from utils.supabase_helpers import get_distinct_values
from backend.backoffice import fetch_price_view
from utils.auth import current_user
from datetime import datetime

user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")


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

col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input("Start Date", value=None)

with col2:
    end_date = st.date_input("End Date", value=None)

start_date = (
    datetime.combine(start_date, datetime.min.time()).isoformat()
    if start_date else None
)

end_date = (
    datetime.combine(end_date, datetime.max.time()).isoformat()
    if end_date else None
)



filters = {
    "department": department,
    "category": category,
    "brand": brand,
    "start_date": start_date,
    "end_date": end_date
}

# start_date = datetime.combine(start_date, datetime.min.time()) if start_date else None
# end_date = datetime.combine(end_date, datetime.max.time()) if end_date else None

if st.button("Search"):
    fetched_data = fetch_price_view(filters)
    st.dataframe(fetched_data)