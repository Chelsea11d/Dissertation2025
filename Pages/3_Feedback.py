import streamlit as st
import pandas as pd
import os

st.title("💬 Feedback")

# Absolute path to feedback file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(BASE_DIR, "feedback.csv")

# Initialize file if not exists
if not os.path.exists(file):
    pd.DataFrame(columns=["Email", "Feedback"]).to_csv(file, index=False)

# Feedback form
email = st.text_input("Your Email (optional)")
feedback = st.text_area("Your Feedback:")

if st.button("Submit Feedback"):
    if feedback.strip():  # only save if not empty
        df = pd.read_csv(file)
        new_entry = pd.DataFrame([{"Email": email, "Feedback": feedback}])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file, index=False)
        st.success("✅ Thank you for your feedback!")
        st.write("📌 Saved Feedback Preview:")
        st.dataframe(new_entry)
    else:
        st.warning("⚠️ Please enter some feedback before submitting.")

# Download section
st.subheader("📥 Download Feedback Data")
feedback_df = pd.read_csv(file)

if not feedback_df.empty:
    csv = feedback_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Feedback CSV",
        data=csv,
        file_name="feedback.csv",
        mime="text/csv",
    )
else:
    st.info("No feedback available yet.")
