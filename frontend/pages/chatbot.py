import streamlit as st
from backend.agents.student_counsellor import StudentCounsellorAgent
from backend.agents.studen_loan_agent import StudentLoanAgent
from backend.agents.admisson_officer_agent import AdmissionOfficerAgent
from backend.data.database import get_collection

# Initialize agents
counsellor = StudentCounsellorAgent()
loan_agent = StudentLoanAgent()
officer = AdmissionOfficerAgent()

# Retrieve student metadata by name
def get_student_metadata_by_name(name):
    students = get_collection("students").get()
    for idx, meta in enumerate(students.get("metadatas", [])):
        if meta.get("name", "").lower() == name.lower():
            return meta
    return None

# Main chatbot function
def display_admission_chatbot(student_name=None):
    st.title("🎓 University Admission Chatbot")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hi! I'm your Admission Assistant 🤖. How can I help you today?"}
        ]

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask anything about admissions, loans, documents, or progress..."):
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            student_meta = get_student_metadata_by_name(student_name) if student_name else None
            student_id = student_meta.get("id") if student_meta else None

            response = "I'm not sure how to help with that."

            if any(word in prompt.lower() for word in ["loan", "finance", "fee"]):
                response = loan_agent.process_loan_request(student_id or "unknown", prompt).get("response")

            elif any(word in prompt.lower() for word in ["status", "stage", "progress"]):
                task = counsellor.create_communication_task(student_id, "current stage")
                response = task.execute().output if task else "Unable to retrieve your admission stage."

            elif any(word in prompt.lower() for word in ["application", "overview", "report", "summary"]):
                task = officer.create_overview_task()
                response = task.execute().output if task else "Unable to generate an admission summary."

            elif any(word in prompt.lower() for word in ["bottleneck", "problem", "delay"]):
                response = officer.detect_admission_bottlenecks()

            elif any(word in prompt.lower() for word in ["message", "communicate", "talk"]):
                response = counsellor.generate_communication_message(student_id, "application stage")

            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
