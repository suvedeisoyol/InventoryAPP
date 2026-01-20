from backend.client import get_client

supabase = get_client()

def get_distinct_values(table: str, column: str, filters: dict | None = None):
    """
    Returns distinct values from a column, optionally filtered by other columns.

    Parameters:
        table (str): The name of the table.
        column (str): The column to get distinct values from.
        filters (dict | None): Optional filters as a dictionary of column-value pairs.

    Returns:
        list: Distinct values from the column
    """
    query = supabase.table(table).select(column)

    if filters:
        for key, value in filters.items():
            query = query.eq(key, value)

    result = query.execute()

    if not result.data:
        return []

    # Deduplicate in Python
    return sorted({row[column] for row in result.data})


def barcode_checker(barcode: str) -> bool:
    """
    Checks if a barcode already exists in the 'variants' table.

    Parameters:
        barcode (str): The barcode to check.
        """
    
    result = supabase.table("variants").select("barcode").eq("barcode", barcode).execute()
    
    return len(result.data) > 0

def variant_finder(dictionary: dict) -> list:
    """
    Finds variants based on provided filters.

    Parameters:
        dictionary (dict): A dictionary of column-value pairs to filter by.

    Returns:
        list: List of matching variants.
    """
    query = supabase.table("variants").select("*")

    for key, value in dictionary.items():
        query = query.eq(key, value)

    result = query.execute()

    return result.data if result.data else []

def product_finder(dictionary: dict) -> list:
    """
    Finds products based on provided filters.

    Parameters:
        dictionary (dict): A dictionary of column-value pairs to filter by.

    Returns:
        list: List of matching products.
    """
    query = supabase.table("products").select("*")

    for key, value in dictionary.items():
        query = query.eq(key, value)

    result = query.execute()

    return result.data if result.data else []