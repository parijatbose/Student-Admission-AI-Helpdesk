import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from datetime import datetime
from backend.data.database import get_collection, initialize_collections
import uuid

# Initialize collections once at startup
initialize_collections()

# Streamlit UI
st.title("Student Admission Form")

# Input fields
name = st.text_input("Full Name")
biometric = st.text_area("Biometric Info (Optional)", placeholder="Biometric data like fingerprint ID or retina scan")
email = st.text_input("Email")
phone = st.text_input("Phone Number")

# Academic Details
st.subheader("Enter Academic Details")
marks_10 = st.number_input("10th Marks (out of 100)", min_value=0, max_value=100)
marks_12 = st.number_input("12th Marks (out of 100)", min_value=0, max_value=100)
aadhar_no = st.text_input("Aadhar Number")
income_category = st.text_input("Income Category (e.g., General, OBC, SC/ST)")

# Loan Request
st.subheader("Loan Request")
loan_amount = st.number_input("Requested Loan Amount", min_value=0.0, step=1000.0)
loan_purpose = st.text_input("Loan Purpose")

if st.button("Submit Application"):
    # Generate unique IDs
    student_id = str(uuid.uuid4())
    app_id = str(uuid.uuid4())
    loan_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    # Student data (no lists in metadata)
    student_data = {
        "id": student_id,
        "name": name,
        "email": email,
        "phone": phone,
        "biometric": biometric,
        "application_id": app_id,
        "communication_history": ""  # list replaced with empty string
    }
    get_collection("students").add(
        documents=[student_id],
        metadatas=[student_data],
        ids=[student_id]
    )

    # Application data (flattened fields)
    application_data = {
        "id": app_id,
        "student_id": student_id,
        "submission_date": now,
        "status": "submitted",
        "eligible": False,
        "marks_10": marks_10,
        "marks_12": marks_12,
        "aadhar_no": aadhar_no,
        "income_category": income_category,
        "updated_on": now
    }
    get_collection("applications").add(
        documents=[app_id],
        metadatas=[application_data],
        ids=[app_id]
    )

    # Loan request data
    loan_data = {
        "id": loan_id,
        "student_id": student_id,
        "amount_requested": loan_amount,
        "purpose": loan_purpose,
        "status": "requested",
        "evaluation_notes": "",
        "evaluated_by": "",
        "decision_date": ""
    }
    get_collection("loan_requests").add(
        documents=[loan_id],
        metadatas=[loan_data],
        ids=[loan_id]
    )

    st.success("Application Submitted Successfully!")
chatbot_url = "http://localhost:8501/streamlit_app"
st.markdown(f"[Go to Chatbot Assistant 🎓]({chatbot_url})", unsafe_allow_html=True)
