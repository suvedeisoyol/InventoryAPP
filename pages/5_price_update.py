import streamlit as st
from utils.layout import page_header
from utils.supabase_helpers import variant_finder, barcode_checker, product_finder
from utils.validators import validate_barcode


from utils.auth import current_user
user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")

page_header("💲 Updating Price")

barcode_to_check = st.text_input("ENTER the Barcode")

if not validate_barcode(barcode_to_check):
    st.error("Invalid barcode")

else:
    if barcode_checker(barcode_to_check):
        st.success("Product found! ready to update price.")
        found_variant = variant_finder({"barcode": barcode_to_check})[0]
        found_product = product_finder({"id": found_variant["product_id"]})[0]
        st.write("### Existing Product Details")
        st.write(f"**Product Name:** {found_product['product']}       **Color/Type:** {found_variant['variant']}")  
    
        price = st.number_input("Price", step=0.01, format="%.2f", value = None, placeholder = "Enter price")
        if st.button("Update Price"):
            from backend.price_update import update_price
            update_price({
                "barcode": barcode_to_check,
                "price": price,
                "updated_by": user["id"]
            })
            st.success(f"Price for barcode '{barcode_to_check}' updated successfully!")
    else:
        st.error("Please input the ITEM details below to add the variant.")