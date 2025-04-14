from crewai import Agent, Task
from langchain.tools import Tool
from backend.utils.gemini_client import get_gemini_client
from backend.data.database import get_collection


class DocumentCheckingAgent:
    def __init__(self):
        self.gemini = get_gemini_client()

    def verify_documents(self, application_id: str):
        try:
            collection = get_collection("applications")
            data = collection.get(ids=[application_id])
            if not data["metadatas"]:
                return "Application not found."

            application = data["metadatas"][0]
            documents = application.get("documents", {})
            required_documents = [
                "identity_proof",
                "transcripts",
                "residence_proof",
                "photo",
                "income_certificate"
            ]
            document_status = {
                doc: "valid" if doc in documents else "missing"
                for doc in required_documents
            }

            response = self.gemini.generate_content(
                f"""You are verifying documents for student {application['student_name']}:
                {documents}

                Required:
                - Identity Proof
                - Transcripts
                - Residence Proof
                - Photo
                - Income Certificate

                Return:
                {{
                  "application_id": "{application_id}",
                  "student_name": "{application['student_name']}",
                  "documents_status": {document_status},
                  "overall_status": "complete/incomplete/flagged",
                  "comments": "..."
                }}
                """
            )

            return response.text
        except Exception as e:
            return f"Error during document verification: {e}"

    def get_agent(self):
        return Agent(
            role="Document Checking Agent",
            goal="Ensure all required admission documents are present and valid.",
            backstory="""You are a detail-focused checker ensuring every applicant's documents 
                         meet university standards before progressing their application.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                Tool.from_function(
                    func=self.verify_documents,
                    name="VerifyDocuments",
                    description="Checks if the submitted application documents are valid and complete."
                )
            ]
        )

    def create_verification_task(self, application_id: str):
        return Task(
            description=f"""Verify the submitted documents for application ID: {application_id}.
            Check for:
            - Identity Proof
            - Transcripts
            - Residence Proof
            - Passport Photo
            - Income Certificate

            Ensure all are present and valid. Return JSON of status per document and overall status.""",
            expected_output="A structured JSON verification report with completeness and comments.",
            agent=self.get_agent()
        )
