import streamlit as st
import pandas as pd
import os

st.title("Feedback 💬")
file = "feedback.csv"
if not os.path.exists(file):
    pd.DataFrame(columns=["Email","Feedback"]).to_csv(file,index=False)

email = st.text_input("Your Email (optional)")
feedback = st.text_area("Your Feedback:")

if st.button("Submit Feedback"):
    df = pd.read_csv(file)
    df = pd.concat([df,pd.DataFrame([{"Email":email,"Feedback":feedback}])], ignore_index=True)
    df.to_csv(file,index=False)
    st.success("✅ Thank you for your feedback!")

import pandas as pd
import streamlit as st

# Load feedback data
try:
    feedback_df = pd.read_csv("feedback.csv")
except FileNotFoundError:
    feedback_df = pd.DataFrame(columns=["Email", "Feedback"])

st.subheader(" Download Feedback Data")

if not feedback_df.empty:
    # Convert to CSV for download
    csv = feedback_df.to_csv(index=False).encode("utf-8")
    
    st.download_button(
        label="Download Feedback CSV",
        data=csv,
        file_name="feedback.csv",
        mime="text/csv",
    )
else:
    st.info("No feedback available yet.")
