from .client import get_client
import uuid
from datetime import datetime

supabase = get_client()

def add_product(data):
    data["id"] = str(uuid.uuid4())
    data["created_at"] = datetime.utcnow().isoformat()
    return supabase.table("products").insert(data).execute()


def get_products(filters: dict | None = None):
    query = supabase.table("products").select("*")

    if filters:
        for column, value in filters.items():
            query = query.eq(column, value)

    return query.execute().data



def fetch_products_with_variants(
    department=None,
    category=None,
    brand=None,
    barcode=None
):
    """
    Calls the Supabase SQL function get_products_with_variants_filtered
    and returns the combined product + variant data.
    Any filter left as None will be ignored by the SQL function.
    """

    payload = {
        "in_department": department,
        "in_category": category,
        "in_brand": brand,
        "in_barcode": barcode
    }

    response = supabase.rpc("get_products_with_variants_filtered", payload).execute()

    if response.data is None:
        return []

    return response.data



