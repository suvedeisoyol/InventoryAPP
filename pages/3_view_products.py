import streamlit as st
from backend.products import get_products
from utils.layout import page_header

from utils.auth import current_user
user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")

page_header("📦 All Products")

products = get_products()

if not products:
    st.info("No products found.")
else:
    st.dataframe(products)
