# frontend/streamlit_app.py

import streamlit as st
from frontend.pages.chatbot import display_admission_chatbot

st.set_page_config(page_title="University Admission Assistant", page_icon="🎓")

st.title("🎓 University Admission Assistant Chatbot")
st.markdown("""
Welcome! This assistant can help you with:
- 📄 Application status
- 📑 Document requirements
- 🧮 Eligibility criteria
- 💰 Student loan inquiries
- 💬 Any other admission-related questions!
""")

# Call the chatbot interface
display_admission_chatbot(student_name="Suryangshu Ghosh")  # Or just: display_admission_chatbot()

