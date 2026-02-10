import streamlit as st
import pandas as pd
from utils.auth import current_user
from backend.inventory import add_inventory_row, add_inventory_movement
from utils.dataframe_store import init_inventory_df
from utils.supabase_helpers import variant_finder, product_finder

user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")

# Initialize DF once
init_inventory_df()

barcode = st.text_input("Barcode", placeholder="Enter barcode to update inventory")

if barcode:
    variant_info = variant_finder({"barcode": barcode})[0]
    product_info = product_finder({"id": variant_info["product_id"]})[0]

    selected_label = (
        f"{product_info['brand']} "
        f"{product_info['product']} {product_info['size']} "
        f"({variant_info['variant']})"
    )

    new_inventory = st.number_input("New Inventory", step=1, format="%d")

    if st.button("Update Inventory"):
        add_inventory_row(
            barcode=barcode,
            product_label=selected_label,
            quantity=new_inventory,
            variant_id=variant_info["id"]
        )

    

st.session_state.inventory_df = st.data_editor(st.session_state.inventory_df)

if st.button("save inventory to database"):
    st.write("Saving inventory to database...")
    for index, row in st.session_state.inventory_df.iterrows():
        st.write(f"Saving row {index}: {row.to_dict()}")
        # Here you would add your logic to save the row to the database
        # For example:
        # save_inventory_to_db(row.to_dict())
        add_inventory_movement(
            variant_id=row["variant_id"],
            quantity_change=row["quantity"],
            updated_by=user["id"]
        )

    
    st.session_state.inventory_df = st.session_state.inventory_df.iloc[0:0]
