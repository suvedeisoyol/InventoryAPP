from backend.products import get_products
from utils.supabase_helpers import get_distinct_values, price_finder, product_finder, variant_finder
from .client import get_client
import streamlit as st


supabase = get_client()

def fetch_price_view(filters: dict):
    payload = {
        "in_department": filters.get("department"),
        "in_category": filters.get("category"),
        "in_brand": filters.get("brand"),
        "in_subbrand": filters.get("subbrand"),
        "in_product": filters.get("product"),
        "in_variant": filters.get("variant"),
        "in_barcode": filters.get("barcode"),
        "in_start_date": filters.get("start_date"),
        "in_end_date": filters.get("end_date"),
        "limit_rows": filters.get("limit_rows", 200)
    }

    response = supabase.rpc("backoffice_update", payload).execute()
    return response.data or []

def product_look_barcode(barcode):
    found_variant = variant_finder({"barcode": barcode})[0]
    found_product = product_finder({"id": found_variant["product_id"]})[0]
    found_price = price_finder({"barcode": barcode})[0]
    return {
        "product_name": f"{found_product['brand']} {found_product['product']}  {found_product['size']}",
        "variant": found_variant['variant'],
        "current_price": found_price['price']
    }

def get_product_filters():
        departments = get_distinct_values("products", "department")
        department = st.selectbox("Department", [""] + departments)

        categories = get_distinct_values("products", "category", filters={"department": department})
        category = st.selectbox("Select Category", [""] + categories)
        brands = get_distinct_values("products", "brand", filters={"department": department, "category": category})
        brand = st.selectbox("Select Brand", [""] + brands)
        subbrands = get_distinct_values("products", "subbrand", filters={"department": department, "category": category, "brand": brand})
        subbrand = st.selectbox("Select Subbrand", [""] + subbrands)
        size = st.selectbox("Select Size", get_distinct_values("products", "size", filters={"department": department, "category": category, "brand": brand, "subbrand": subbrand}))


        filter = {
            "department": department,
            "category": category,
            "brand": brand,
            "subbrand": subbrand,
            #"product": product_name,
            "size": size}
        
        return filter

def find_product_id():
    filters = get_product_filters()
    products = get_products(filters=filters)
    product_labels = {
    f"{p['product']} ({p['brand']} - {p['size']})": p["id"]
    for p in products
    }

    selected_label = st.selectbox("Select Product", list(product_labels.keys()))
    if selected_label:
        product_id = product_labels[selected_label]
        return product_id
    else:
        return None