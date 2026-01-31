from .client import get_client


supabase = get_client()

def fetch_price_view(filters: dict):
    payload = {
        "in_department": filters.get("department"),
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
