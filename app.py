import streamlit as st
import pandas as pd

# Load product data
df = pd.read_csv("vegan_products.csv")

st.title("AI-Powered Nutrition App for Vegans")

st.markdown("Select your nutrition preferences:")

# User preferences
pref_protein = st.checkbox('Protein')
pref_carbs = st.checkbox('Carbs')
pref_sugar = st.checkbox('Sugar')
pref_fats = st.checkbox('Fats')
pref_vitamins = st.checkbox('Vitamins')
pref_minerals = st.checkbox('Minerals')

selected_prefs = []
if pref_protein: selected_prefs.append('Protein')
if pref_carbs: selected_prefs.append('Carbs')
if pref_sugar: selected_prefs.append('Sugar')
if pref_fats: selected_prefs.append('Fats')
if pref_vitamins: selected_prefs.append('Vitamins')
if pref_minerals: selected_prefs.append('Minerals')

if selected_prefs:
    st.subheader(" Products matching your preferences")

    # Filter: products that have >0 in selected nutrients
    filtered_df = df.copy()
    for col in selected_prefs:
        filtered_df = filtered_df[filtered_df[col] > 0]

    # Show table with option to select products
    selected_products = st.multiselect(
        "Select products to add to your day:",
        filtered_df['Name']
    )

    # Quantities
    product_quantities = {}
    for product in selected_products:
        qty = st.number_input(f"Quantity for {product} (servings)", min_value=1, value=1)
        product_quantities[product] = qty

    # Calculate total nutrition
    if selected_products:
        st.subheader(" Nutrition summary")
        totals = {col: 0 for col in selected_prefs}
        for product in selected_products:
            qty = product_quantities[product]
            row = df[df['Name'] == product]
            for col in selected_prefs:
                totals[col] += row.iloc[0][col] * qty

        st.write("Total nutrition based on your selection:")
        for col, total in totals.items():
            st.write(f"{col}: {total} g")

        # Check against daily goals (example: protein goal = 50g)
        protein_goal = 50
        if 'Protein' in selected_prefs:
            protein_intake = totals.get('Protein', 0)
            if protein_intake < protein_goal:
                st.warning(f"⚠️ You’re missing {protein_goal - protein_intake}g of protein today! Consider adding more protein-rich items.")

        # Show recommendations
        st.subheader("✨ Recommended extras")
        extra_proteins = df[(df['Protein'] >= 8) & (~df['Name'].isin(selected_products))]
        if not extra_proteins.empty:
            st.write("High-protein options you might like:")
            st.dataframe(extra_proteins[['Name', 'Protein']])
else:
    st.info("Please select at least one nutrition preference to get started!")
