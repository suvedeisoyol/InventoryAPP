import streamlit as st
from backend.backoffice import fetch_price_view, find_product_id, get_product_filters

#from backend.backoffice import 
from backend.products import get_products

import pandas as pd
from utils.auth import current_user
from backend.inventory import add_inventory_row, add_inventory_movement, add_inventory_movements, get_current_inventory, get_current_stocking
from utils.dataframe_store import init_inventory_df
from utils.supabase_helpers import get_distinct_values, variant_finder, product_finder

user = current_user()
if not user:
    st.switch_page("pages/0_Login.py")

tab_lists = ["Adding Inventory", "Stocking", "Inventory Analysis"]

inventory_tab, stocking_tab, analysis_tab = st.tabs(tab_lists)


with inventory_tab:
    # Initialize DF once
    init_inventory_df()

    subtab1, subtab2 = st.tabs(["Update Inventory by Barcode", "Bulk Inventory Update"])
    with subtab1:

        barcode = st.text_input("Barcode", placeholder="Enter barcode to update inventory")

        if barcode:
            variant_info = variant_finder({"barcode": barcode})[0]
            product_info = product_finder({"id": variant_info["product_id"]})[0]

            selected_label = (
                f"{product_info['brand']} "
                f"{product_info['product']} {product_info['size']} "
                f"({variant_info['variant']})"
            )
            st.write(f"Selected Product: **{selected_label}**")
            new_inventory = st.number_input("New Inventory", step=1, format="%d")

            if st.button("Update Inventory"):
                add_inventory_row(
                    barcode=barcode,
                    product_label=selected_label,
                    quantity=new_inventory,
                    variant_id=variant_info["id"]
                )
        st.session_state.inventory_df = st.data_editor(st.session_state.inventory_df)

        if st.button("Save Receiving Changes"):
            st.write("Saving receiving changes...")

            movements = [
                {
                    "variant_id": row["variant_id"],
                    "quantity_change": row["quantity"],
                    "updated_by": user["id"],
                    "stocked": True
                }
                for _, row in st.session_state.inventory_df.iterrows()
                if pd.notna(row["quantity"]) 
                    and isinstance(row["quantity"], (int)) 
                    and row["quantity"] != 0
            ]

            add_inventory_movements(movements)   # <-- clean call

            st.success("Receiving changes saved successfully!")

        
            st.session_state.inventory_df = st.session_state.inventory_df.iloc[0:0]

    with subtab2:
        st.write("Bulk Inventory Update")
        
        id = find_product_id()
        if id != None:
            st.write(f"Selected Product ID: {id}")
            data = variant_finder({"product_id": id})
            

            inventory_data = pd.DataFrame(data)   
            inventory_data["Receiving"] = 0

            inventory_data = st.data_editor(inventory_data, column_config = {
                "variant": st.column_config.TextColumn(disabled=True),
                "barcode": st.column_config.TextColumn(disabled=True),
                "Receiving": st.column_config.NumberColumn(min_value=0, step=1)},
                column_order=["variant", "barcode", "Receiving"]
            )

        if st.button("Save Receiving Bulk Changes"):
            st.write("Saving receiving changes...")

            movements = [
                {
                    "variant_id": row["id"],
                    "quantity_change": row["Receiving"],
                    "updated_by": user["id"],
                    "stocked": True
                }
                for _, row in inventory_data.iterrows()
                if pd.notna(row["Receiving"]) 
                    and isinstance(row["Receiving"], (int)) 
                    and row["Receiving"] != 0
            ]

            add_inventory_movements(movements)   # <-- clean call

            st.success("Receiving changes saved successfully!")


        

    

with stocking_tab:
    col1, col2, col3 = st.columns(3)
    departments= ["HAIR", "WIG", "CHEMICAL", "GENERAL"] 
    with col1:
        department = st.selectbox("Departments", [""] + departments)
        department = department or None
        
        categories = get_distinct_values("products", "category", filters={"department": department})

    with col2:
        category = st.selectbox("Category", [""] + categories)
        category = category or None

        brands = get_distinct_values("products", "brand", filters={"department": department, "category": category})
    with col3:
        brand = st.selectbox("Select the Brand", [""] + brands )
        brand = brand or None
    
    filters = {
    "department": department,
    "category": category,
    "brand": brand,
}
    inventory_data = get_current_inventory(filters)
    inventory_data = pd.DataFrame(inventory_data)   
    inventory_data["Stocking"] = 0
    inventory_data = st.data_editor(inventory_data)


    if st.button("Save Stocking Changes"):
        st.write("Saving stocking changes...")

        movements = [
            {
                "variant_id": row["variant_id"],
                "quantity_change": -1 * row["Stocking"],
                "updated_by": user["id"],
                "stocked": False
            }
            for _, row in inventory_data.iterrows()
            if pd.notna(row["Stocking"]) 
                and isinstance(row["Stocking"], (int)) 
                and row["Stocking"] != 0
        ]

        add_inventory_movements(movements)   # <-- clean call

        st.success("Stocking changes saved successfully!")

    if st.button("Load Current Stocking"):
        filters["stocked"] = False
        stocking_data = get_current_inventory(filters)
        stocking_data = pd.DataFrame(stocking_data)
        st.dataframe(stocking_data)




with analysis_tab:
    st.write("Inventory Analysis coming soon!")
    
    import pandas as pd

    df = pd.DataFrame({
        "item": ["apple", "banana", "orange"],
        "quantity": [10, 20, 15]
    })

    new_quantities = []

    for i, row in df.iterrows():
        st.write(row["item"])
        qty = st.number_input(
            "Quantity",
            value=row["quantity"],
            key=f"qty_{i}"
        )
        new_quantities.append(qty)

    df["quantity"] = new_quantities

    st.write(df)

    import pandas as pd

    df = pd.DataFrame({
        "item": ["apple", "banana", "orange"],
        "price": [1.2, 0.8, 1.5],
        "quantity": [10, 20, 15]
    })

    edited_df = st.data_editor(
        df,
        column_config={
            "item": st.column_config.TextColumn(disabled=True),
            "price": st.column_config.NumberColumn(disabled=True),
            "quantity": st.column_config.NumberColumn(disabled=False)
        },
        hide_index=True
    )

    st.write("Updated DataFrame:")
    st.dataframe(edited_df)


