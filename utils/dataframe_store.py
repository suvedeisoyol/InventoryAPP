import streamlit as st
import pandas as pd

def init_inventory_df():
    if "inventory_df" not in st.session_state:
        st.session_state.inventory_df = pd.DataFrame(
            columns=["barcode", "Product", "quantity", "variant_id"]
        )
