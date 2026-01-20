from .client import get_client
import uuid
from datetime import datetime

supabase = get_client()

def create_price(data):
    """Creates a new price entry in the 'prices' table."""

    data["created_at"] = datetime.utcnow().isoformat()

    query = supabase.table("prices").insert(data)

    return query.execute()


def update_price(data):
    """Updates the price of a product in the 'prices' table based on the barcode."""

    query = supabase.table("prices").update({
        "price": float(data["price"]),
        "updated_at": datetime.utcnow().isoformat()
    }).eq("barcode", data["barcode"])

    return query.execute()
