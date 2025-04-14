# main.py

import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# Updated import for ChromaDB-based initialization
from backend.data.database import initialize_collections

# Agents using ChromaDB-based logic
from backend.agents.admisson_officer_agent import AdmissionOfficerAgent
from backend.agents.document_checking_agent import DocumentCheckingAgent
from backend.agents.shortlisting_agent import ShortlistingAgent
from backend.agents.student_counsellor import StudentCounsellorAgent
from backend.agents.studen_loan_agent import StudentLoanAgent

# Initialize FastAPI app
app = FastAPI(title="University Admission System API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB collections
initialize_collections()

# Initialize Agents
admission_officer = AdmissionOfficerAgent()
document_checker = DocumentCheckingAgent()
shortlisting_agent = ShortlistingAgent()
student_counsellor = StudentCounsellorAgent()
loan_agent = StudentLoanAgent()

# Root route
@app.get("/")
async def root():
    return {"message": "University Admission System is running"}

# Get all applications
@app.get("/applications")
async def get_all_applications():
    return admission_officer.get_all_applications()

# Get specific application details
@app.get("/applications/{application_id}")
async def get_application(application_id: str):
    return admission_officer.get_application_details(application_id)

# Verify documents for a specific application
@app.post("/applications/{application_id}/verify-documents")
async def verify_documents(application_id: str):
    return document_checker.verify_documents(application_id)

# Shortlist an application based on eligibility
@app.post("/applications/{application_id}/shortlist")
async def shortlist_application(application_id: str):
    return shortlisting_agent.evaluate_and_shortlist(application_id)

# Send a message to a student
@app.post("/students/{student_id}/communicate")
async def communicate_with_student(student_id: str, message: dict):
    return student_counsellor.send_message(student_id, message["content"])

# Process loan request from a student
@app.post("/students/{student_id}/loan-request")
async def process_loan(student_id: str, loan_data: dict):
    return loan_agent.process_loan_request(student_id, loan_data)

# Get overall admission dashboard/status
@app.get("/admission/status")
async def get_admission_dashboard():
    return admission_officer.get_admission_status()

# Chat endpoint for chatbot interaction
@app.post("/chat")
async def chat_endpoint(message: dict):
    application_id = message.get("application_id")  # Optional context
    return admission_officer.process_chat_message(message["content"], application_id)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
