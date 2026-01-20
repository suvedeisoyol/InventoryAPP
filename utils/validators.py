from backend.client import get_client

supabase = get_client()

def validate_barcode(barcode: str) -> bool:
    if not barcode:
        return False
    if len(barcode) < 6:
        return False
    return True


def barcode_checker(barcode: str) -> bool:
    """
    Checks if a barcode already exists in the 'variants' table.

    Parameters:
        barcode (str): The barcode to check.
        """
    
    result = supabase.table("variants").select("barcode").eq("barcode", barcode).execute()
    
    return len(result.data) > 0