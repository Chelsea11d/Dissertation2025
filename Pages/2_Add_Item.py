import streamlit as st
import pandas as pd
import os

st.title("Add Missing Product 🛒")
file = "user_suggestions.csv"
if not os.path.exists(file):
    pd.DataFrame(columns=["Email","Name","Category","Protein","Carbs","Sugar","Fats","Vitamins","Minerals"]).to_csv(file,index=False)

email = st.text_input("Your Email (optional)")

name = st.text_input("Product Name")
category_options = ["Protein", "Carb", "Ready Meal", "Spread", "Drink", "Dessert", "Snack", "Other"]
category = st.selectbox("Select Product Category", category_options)

# If user selects "Other", allow custom input
if category == "Other":
    category = st.text_input("Enter custom category")
protein = st.number_input("Protein (g per 100g)", min_value=0)
carbs = st.number_input("Carbs (g per 100g)", min_value=0)
sugar = st.number_input("Sugar (g per 100g)", min_value=0)
fats = st.number_input("Fats (g per 100g)", min_value=0)
vitamins = st.slider("Vitamins (score 1–5)", 0, 5, 0)
minerals = st.slider("Minerals (score 1–5)", 0, 5, 0)

if st.button("Submit"):
    new_entry = {"Email":email,"Name":name,"Category":category,
                 "Protein":protein,"Carbs":carbs,"Sugar":sugar,"Fats":fats,
                 "Vitamins":vitamins,"Minerals":minerals}
    df = pd.read_csv(file)
    df = pd.concat([df,pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(file,index=False)
    st.success("✅ Product suggestion submitted!")
else:
        st.warning("⚠️ Please fill in at least the product name and category.")    

# --- Suggestions download ---
try:
    suggestions_df = pd.read_csv("suggestions.csv")
except FileNotFoundError:
    suggestions_df = pd.DataFrame(columns=["Email", "Suggested Item"])

st.subheader("Download User Suggestions")

if not suggestions_df.empty:
    csv_suggestions = suggestions_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Suggestions CSV",
        data=csv_suggestions,
        file_name="suggestions.csv",
        mime="text/csv",
    )
else:
    st.info("No suggestions submitted yet.")