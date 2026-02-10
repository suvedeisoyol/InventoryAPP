import streamlit as st
from backend.client import get_client

supabase = get_client()
def add_inventory_row(barcode, product_label, quantity, variant_id):
    st.session_state.inventory_df.loc[len(st.session_state.inventory_df)] = {
        "barcode": barcode,
        "Product": product_label,
        "quantity": quantity,
        "variant_id": variant_id,
    }



def add_inventory_movement(variant_id, quantity_change, updated_by):
    """
    Inserts a new inventory movement row into Supabase.
    quantity_change can be positive (add stock) or negative (remove stock).
    """

    from backend.client import get_client
    supabase = get_client()

    return supabase.table("inventory_movements").insert({
        "variant_id": variant_id,
        "quantity_change": quantity_change,
        "updated_by": updated_by
    }).execute()
