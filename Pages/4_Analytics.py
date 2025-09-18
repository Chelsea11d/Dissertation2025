import streamlit as st
import pandas as pd

st.title("Analytics 📊")

# Load product data
df_products = pd.read_csv("vegan_products_expanded.csv")

# Load user suggestions if exists
try:
    df_suggestions = pd.read_csv("user_suggestions.csv")
except FileNotFoundError:
    df_suggestions = pd.DataFrame(columns=["Name", "Category", "Protein", "Carbs", "Sugar", "Fats", "Vitamins", "Minerals"])

# Load user intake logs (you can create a CSV to store daily intakes)
try:
    df_intake = pd.read_csv("user_intake.csv")
except FileNotFoundError:
    df_intake = pd.DataFrame(columns=["Name","Protein","Carbs","Sugar","Fats","Vitamins","Minerals","Quantity"])

# --- 1️⃣ Total nutrients consumed vs goals ---
st.subheader("1️⃣ Total Nutrients Consumed vs Daily Goals")

if not df_intake.empty:
    # Sum total intake
    total_intake = df_intake[['Protein','Carbs','Sugar','Fats','Vitamins','Minerals']].sum()
    daily_goals = {'Protein':50,'Carbs':275,'Sugar':50,'Fats':70,'Vitamins':5,'Minerals':5}

    # Create comparison DataFrame
    comparison_df = pd.DataFrame({
        'Consumed': total_intake,
        'Goal': pd.Series(daily_goals)
    })

    st.bar_chart(comparison_df)
    
    # Show alerts for missing nutrients
    missing = comparison_df['Goal'] - comparison_df['Consumed']
    missing = missing[missing > 0]
    if not missing.empty:
        st.warning("⚠️ Nutrients you are missing:")
        for nutrient, amt in missing.items():
            st.write(f"- {nutrient}: {round(amt,1)} units")
    else:
        st.success("🎉 All nutrient goals met!")
else:
    st.info("No user intake data yet. Track your nutrients in the Nutrition Tracker page.")

# --- 2️⃣ Popular Products ---
st.subheader("2️⃣ Popular Products")

# Count product selections from intake and suggestions
product_counts = pd.concat([
    df_intake['Name'] if not df_intake.empty else pd.Series(),
    df_suggestions['Name'] if not df_suggestions.empty else pd.Series()
]).value_counts()

if not product_counts.empty:
    top_products = product_counts.head(10)
    st.bar_chart(top_products)
else:
    st.info("No product selections or suggestions yet.")

# --- 3️⃣ Additional Insights ---
st.subheader("3️⃣ Additional Insights")
st.markdown("""
- You can use this page to **visualize your daily nutrient intake**.  
- **Popular products** help you see what other users are consuming or suggesting.  
- **Missing nutrient alerts** guide you to balance your vegan diet.
""")
