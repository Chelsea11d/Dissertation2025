import streamlit as st
import pandas as pd


st.set_page_config(
    page_title="Vegan Nutrition App",  # Browser tab title
    page_icon="🌱",                    # Optional icon
    layout="centered",
    initial_sidebar_state="expanded"
)

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
                **Navigate using the sidebar to explore:**
- Nutrition Tracker
                
     1. **Select your nutrition preferences** (Protein, Carbs, Fats, etc.) using the checkboxes.  
     2. The app will show you **vegan products** that contain those nutrients.  
     3. **Choose products** you plan to eat today from the list.  
     4. For each product, enter the **portion size in grams**.  
     5. The app calculates your **total daily intake** and compares it to daily goals.  
     6. If you are **missing key nutrients**, the app alerts you and suggests vegan alternatives.  
     7. Explore the **recommended extras** section for more ideas on balancing your diet!

                
- Add Missing Products
- Feedback
- Analytics
""")

