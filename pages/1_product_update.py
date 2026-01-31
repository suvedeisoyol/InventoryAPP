import streamlit as st

from utils.auth import current_user
user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")





tab_lists = ["Add Product's Name", "Add Product's Variant/Color", "Price Update"]

product_tab, variant_tab, price_tab = st.tabs(tab_lists)


with product_tab:
    from forms.add_product_form import add_product_form
    add_product_form(user)

with variant_tab:
    from forms.add_variant_form import add_variant_form
    add_variant_form(user)

with price_tab:
    from forms.price_update_form import price_update_form
    price_update_form(user)