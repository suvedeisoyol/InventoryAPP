from backend.backoffice import product_look_barcode
import streamlit as st
from utils.layout import page_header
from utils.supabase_helpers import variant_finder, barcode_checker, product_finder, price_finder
from utils.validators import validate_barcode


def price_update_form(user):
    page_header("💲 Updating Price")

    barcode_to_check = st.text_input("ENTER the Barcode")

    if not validate_barcode(barcode_to_check):
        st.error("Invalid barcode")

    else:
        if barcode_checker(barcode_to_check):
            product_found = product_look_barcode(barcode_to_check)
            st.write("### Product Details")
            st.write(f"**Product Name:**  {product_found['product_name']}     **Color/Type:** {product_found['variant']}     **Current Price:** ${product_found['current_price']}") 
            if product_found:
                st.success("Product found! ready to update price.")

            price = st.number_input("New Price", step=.50, format="%.2f", value = product_found['current_price'], placeholder = "Enter price to update")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update Price"):
                    from backend.price_update import update_price
                    update_price({
                        "barcode": barcode_to_check,
                        "price": price,
                        "updated_by": user["id"]
                    })
                    st.success(f"Price for barcode '{barcode_to_check}' updated successfully!")
                    st.write(f"Price inserted {price_finder({'barcode': barcode_to_check})[0]['price']}")
            with col2:
                if st.button("Delete the Variant"):
                    st.warning("Are you sure you want to delete this variant? This action cannot be undone.")
                    if st.button("Confirm Deletion"):
                        from backend.variants import delete_variant
                        delete_variant(barcode_to_check)
                        st.success(f"Variant with barcode '{barcode_to_check}' deleted successfully!")
        else:
            st.error("Please input the ITEM details below to add the variant.")