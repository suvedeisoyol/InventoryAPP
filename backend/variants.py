from .client import get_client
import uuid
from datetime import datetime

supabase = get_client()

def add_variant(data):
    data["id"] = str(uuid.uuid4())
    data["created_at"] = datetime.utcnow().isoformat()
    return supabase.table("variants").insert(data).execute()

def get_variants_by_product(filters: dict | None = None):

    query = supabase.table("variants").select("*")

    if filters:
        for column, value in filters.items():
            query = query.eq(column, value)

    return query.execute().data

