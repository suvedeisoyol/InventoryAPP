import streamlit as st
from backend.variants import add_variant
from backend.products import get_products
from backend.price_update import create_price
from utils.supabase_helpers import get_distinct_values
from utils.validators import validate_barcode
from utils.supabase_helpers import barcode_checker
from utils.supabase_helpers import variant_finder
from utils.supabase_helpers import product_finder
from utils.layout import page_header

from utils.auth import current_user
user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")


barcode_to_check = st.text_input("ENTER the Barcode")

if not validate_barcode(barcode_to_check):
    st.error("Invalid barcode")

else:
    if barcode_checker(barcode_to_check):
        st.error("Barcode already exists")
        found_variant = variant_finder({"barcode": barcode_to_check})[0]
        found_product = product_finder({"id": found_variant["product_id"]})[0]
        st.write("### Existing Product Details")
        st.write(f"**Product Name:** {found_product['product']}       **Color/Type:** {found_variant['variant']}")  
    

    else:
        st.success("Please input the ITEM details below to add the variant.")


page_header("➕ Add Product Variant")


departments = get_distinct_values("products", "department")
department = st.selectbox("Department", departments)

categories = get_distinct_values("products", "category", filters={"department": department})
category = st.selectbox("Select Category", categories)
brands = get_distinct_values("products", "brand", filters={"department": department, "category": category})
brand = st.selectbox("Select Brand", brands)
subbrands = get_distinct_values("products", "subbrand", filters={"department": department, "category": category, "brand": brand})
subbrand = st.selectbox("Select Subbrand", subbrands)
size = st.selectbox("Select Size", get_distinct_values("products", "size", filters={"department": department, "category": category, "brand": brand, "subbrand": subbrand}))

filter = {
    "department": department,
    "category": category,
    "brand": brand,
    "subbrand": subbrand,
    #"product": product_name,
    "size": size}

products = get_products(filters=filter)

product_labels = [
    f"{p['product']} ({p['brand']} - {p['size']})" for p in products]
product_choice = st.selectbox("Product", product_labels)
variant_name = st.text_input("Variant Name", placeholder ="Enter product color/type")
barcode = st.text_input("Barcode", placeholder="Enter barcode")
price = st.number_input("Price", step=0.01, format="%.2f", value = None, placeholder = "Enter price")


if st.button("Add Product Variant"):
    if not products:
        st.error("No matching product found. Please add the product first.")
    elif not validate_barcode(barcode):
        st.error("Invalid barcode")
    else:
        product_id = products[0]["id"]

        add_variant({
            "variant": variant_name.upper(),
            "barcode": barcode,
            "product_id": product_id,
            "hq_price": price,
            "created_by": user["id"]
        })

        create_price({
            "barcode": barcode,
            "price": price,
            "updated_by": user["id"]
        })



        

        st.success(f"Variant '{variant_name}' added successfully!")