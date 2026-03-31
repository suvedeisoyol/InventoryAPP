from itertools import product
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



def add_inventory_movement(variant_id, quantity_change, updated_by, stocked=True):
    """
    Inserts a new inventory movement row into Supabase.
    quantity_change can be positive (add stock) or negative (remove stock).
    stocked is a boolean that is False when the movement is not proceeded from basement to the shelf
    """

    from backend.client import get_client
    supabase = get_client()

    return supabase.table("inventory_movements").insert({
        "variant_id": variant_id,
        "quantity_change": quantity_change,
        "updated_by": updated_by,
        "stocked": stocked
    }).execute()

def add_inventory_movements(movements: list):
    """
    Insert multiple inventory movement rows in one batch.
    """
    if not movements:
        return

    supabase.table("inventory_movements").insert(movements).execute()


def get_current_inventory(filter):
    data = supabase.rpc("get_current_inventory", {
    "in_department": filter.get("department"),
    "in_category": filter.get("category"),
    "in_brand": filter.get("brand"),
    "in_product": filter.get("product"),
    "in_stocked": filter.get("stocked", True)  # Default to True if not provided
    }).execute().data
    return data or []   

def get_current_stocking(filter):
    data = supabase.rpc("get_current_stocking", {
    "in_department": filter.get("department"),
    "in_category": filter.get("category"),
    "in_brand": filter.get("brand") 
    }).execute().data
    return data or []

def temp_changing_stock():
    # This is a temporary function to change the stocking status of inventory movements for testing purposes.
    supabase.table("inventory_movements").update({"stocked": True}).eq("stocked", False).execute()
    return None