import streamlit as st
import pandas as pd

df = pd.read_csv("vegan_products_expanded.csv")

st.title("Nutrition Tracker 🍎")

# Nutrient preferences
st.markdown("### Select your nutrition preferences:")
prefs = ['Protein','Carbs','Sugar','Fats','Vitamins','Minerals']
selected_prefs = [p for p in prefs if st.checkbox(p)]

if selected_prefs:
    filtered_df = df.copy()
    for col in selected_prefs:
        filtered_df = filtered_df[filtered_df[col] > 0]

    selected_products = st.multiselect("Select products to add:", filtered_df['Name'])

    product_quantities = {}
    for product in selected_products:
        qty = st.number_input(f"Portion size for {product} (grams)", min_value=10, step=10, value=100)
        product_quantities[product] = qty

    if selected_products:
        totals = {col:0 for col in selected_prefs}
        for product in selected_products:
            qty = product_quantities[product]
            row = df[df['Name']==product].iloc[0]
            for col in selected_prefs:
                totals[col] += (row[col]*qty)/100

        st.subheader("📊 Nutrition Summary")
        st.dataframe(pd.DataFrame.from_dict(totals, orient='index', columns=['Total Intake']))

        st.subheader("🍽 Selected Products")
        for product, qty in product_quantities.items():
            st.write(f"- {product}: {qty} g")

        # Daily targets
        daily_targets = {'Protein':50,'Carbs':275,'Sugar':50,'Fats':70,'Vitamins':5,'Minerals':5}
        missing = {nutrient: daily_targets[nutrient]-totals[nutrient] 
                   for nutrient in selected_prefs if totals[nutrient]<daily_targets[nutrient]}

        if missing:
            st.warning("⚠️ You're missing:")
            for nutrient, amt in missing.items():
                st.write(f"- {nutrient}: {round(amt,1)} units")
        else:
            st.success("🎉 All nutrient goals met!")

        st.subheader("✨ Recommended Products")
        for nutrient, amt_missing in missing.items():
            candidates = df[~df['Name'].isin(selected_products)]
            candidates = candidates[candidates[nutrient]>0].sort_values(by=nutrient, ascending=False)
            for idx, row in candidates.iterrows():
                grams_needed = (amt_missing/row[nutrient])*100
                st.write(f"To reach your {nutrient} goal, consider **{grams_needed:.0f} g** of **{row['Name']}**")

        st.subheader("📊 Nutrient Progress")
        for nutrient in selected_prefs:
            intake = totals[nutrient]
            goal = daily_targets[nutrient]
            st.write(f"**{nutrient}:** {round(intake,1)}/{goal}")
            st.progress(min(intake/goal,1.0))
else:
    st.info("Select at least one nutrient to start!")
