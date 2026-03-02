import streamlit as st
import pandas as pd

def init_inventory_df():
    if "inventory_df" not in st.session_state:
        st.session_state.inventory_df = pd.DataFrame(
            columns=["barcode", "Product", "quantity", "variant_id"]
        )

def init_stocking_df():
    if "stocking_df" not in st.session_state:
        st.session_state.stocking_df = pd.DataFrame(
            columns=["variant_id", "Product", "Current Inventory", "Stocking"]
        )