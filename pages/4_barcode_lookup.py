import streamlit as st
from backend.variants import get_variants_by_product
from backend.products import get_products
from utils.layout import page_header


from utils.auth import current_user
user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")

page_header("🔍 Barcode Lookup")

barcode = st.text_input("Enter barcode")

if st.button("Search"):
    products = get_products()
    found = None

    for p in products:
        variants = get_variants_by_product(p["id"])
        for v in variants:
            if v["barcode"] == barcode:
                found = (p, v)

    if found:
        product, variant = found
        st.success("Match found!")
        st.write("### Product")
        st.json(product)
        st.write("### Variant")
        st.json(variant)
    else:
        st.error("No product found for this barcode.")
