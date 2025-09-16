import streamlit as st
import pandas as pd

# Load product data
df = pd.read_csv("vegan_products_expanded.csv")

# --- App Introduction ---
st.title("🌱 AI-Powered Nutrition App for Vegans")

st.markdown("""
Welcome to the **AI-Powered Nutrition App for Vegans**!  

This app helps you maintain a balanced vegan diet by tracking your nutrient intake based on the foods you select.  
You can:
- Select your nutrition preferences (Protein, Carbs, Fats, Sugar, Vitamins, Minerals)  
- Choose vegan products you plan to consume today  
- Enter portion sizes in grams (g) for each product  

The app will calculate your total nutrient intake, compare it to daily goals, and give recommendations if you're missing key nutrients.  
All nutrition values are calculated per **100 g of each product**. You can interpret the results using the progress bars and summary tables.
""")

# --- User Manual ---
st.info("""
### ℹ️ How to read nutrition values:
- **Portion Size** → shown in grams (g), actual amount consumed.  
- **Protein, Carbs, Sugar, Fats** → measured in grams (g) per portion.  
- **Vitamins, Minerals** → given as a score from 1–5.  
- Nutrient intake is calculated as:  

    `Nutrient intake = (portion size in grams / 100) * nutrient per 100g`  
    e.g., if Tofu has 10 g protein per 100 g, and you eat 250 g:  
    `250/100 * 10 = 25 g protein`
""")

with st.expander("📖 How to use this app"):
    st.markdown("""
1. **Select your nutrition preferences** (Protein, Carbs, Fats, etc.) using the checkboxes.  
2. The app will show you **vegan products** that contain those nutrients.  
3. **Choose products** you plan to eat today from the list.  
4. For each product, enter the **portion size in grams**.  
5. The app calculates your **total daily intake** and compares it to daily goals.  
6. If you are **missing key nutrients**, the app alerts you and suggests vegan alternatives.  
7. Explore the **recommended extras** section for more ideas on balancing your diet!
""")

st.markdown("----")

# --- User Preferences ---
st.markdown("### Select your nutrition preferences:")
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

# --- Filter and Show Products ---
if selected_prefs:
    st.subheader("📦 Products matching your preferences")
    filtered_df = df.copy()
    for col in selected_prefs:
        filtered_df = filtered_df[filtered_df[col] > 0]

    selected_products = st.multiselect(
        "Select products to add to your day:",
        filtered_df['Name']
    )

    # --- Portion Sizes in grams ---
    product_quantities = {}
    for product in selected_products:
        qty = st.number_input(f"Portion size for {product} (grams)", min_value=10, step=10, value=100)
        product_quantities[product] = qty

    # --- Nutrition Summary ---
    if selected_products:
        st.subheader("📊 Nutrition Summary")
        totals = {col: 0 for col in selected_prefs}
        for product in selected_products:
            qty = product_quantities[product]
            row = df[df['Name'] == product].iloc[0]
            for col in selected_prefs:
                totals[col] += (row[col] * qty) / 100  # scale per 100g

        # Display total intake table
        summary_df = pd.DataFrame.from_dict(totals, orient='index', columns=['Total Intake'])
        st.dataframe(summary_df)

        # Show selected products with portion sizes
        st.subheader("🍽 Selected Products with Portion Sizes")
        for product in selected_products:
            qty = product_quantities[product]
            st.write(f"- {product}: {qty} g")

        # --- Daily goals ---
        daily_targets = {
            'Protein': 50,
            'Carbs': 275,
            'Sugar': 50,
            'Fats': 70,
            'Vitamins': 5,  # score 1-5
            'Minerals': 5   # score 1-5
        }

        # --- Missing Nutrients ---
        missing = {}
        for nutrient in selected_prefs:
            diff = daily_targets[nutrient] - totals[nutrient]
            if diff > 0:
                missing[nutrient] = diff

        # Show missing nutrient warnings
        if missing:
            st.warning("⚠️ You're missing:")
            for nutrient, amt in missing.items():
                st.write(f"- {nutrient}: {round(amt, 2)} units")
        else:
            st.success("🎉 Great! You've met your daily targets!")

        # --- Recommendations for missing nutrients ---
        st.subheader("✨ Recommended Products to Meet Missing Nutrients")
        for nutrient, amt_missing in missing.items():
            candidates = df[~df['Name'].isin(selected_products)]
            candidates = candidates[candidates[nutrient] > 0].sort_values(by=nutrient, ascending=False)
            for idx, row in candidates.iterrows():
                grams_needed = (amt_missing / row[nutrient]) * 100  # per 100g scaling
                st.write(f"To reach your {nutrient} goal, consider **{grams_needed:.0f} g** of **{row['Name']}**")

        # --- Progress Bars for Nutrients ---
        st.subheader("📊 Nutrient Intake Progress")
        for nutrient in selected_prefs:
            intake = totals[nutrient]
            goal = daily_targets[nutrient]
            percent = min(intake / goal, 1.0)  # cap at 100%
            st.write(f"**{nutrient}:** {round(intake, 1)} / {goal} units")
            st.progress(percent)

else:
    st.info("Please select at least one nutrition preference to get started!")
