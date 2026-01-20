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
