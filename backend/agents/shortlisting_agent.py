from crewai import Agent, Task
from langchain.tools import Tool
from backend.utils.gemini_client import get_gemini_client
from backend.data.database import get_collection


class ShortlistingAgent:
    def __init__(self):
        self.gemini = get_gemini_client()

    def get_agent(self):
        """Return the CrewAI agent responsible for application shortlisting."""
        return Agent(
            role="Application Shortlisting Agent",
            goal="Screen applications and shortlist candidates based on eligibility criteria.",
            backstory="""You are a diligent admissions assistant who evaluates applications based on academic scores,
            extracurriculars, and other admission policies. You ensure only eligible and promising candidates are shortlisted.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                Tool.from_function(
                    func=self.shortlist_applications,
                    name="ShortlistApplications",
                    description="Screen applications and determine which candidates should be shortlisted."
                )
            ]
        )

    def create_shortlisting_task(self):
        """Create a task for screening and shortlisting applications"""
        return Task(
            description="""Evaluate student applications for shortlisting.
            Consider:
            - Academic performance
            - Extracurricular activities
            - Compliance with eligibility criteria

            Decide if each student should be shortlisted. Justify each decision.
            Return a structured JSON list.
            """,
            expected_output="A list of shortlisted and rejected applications with reasons.",
            agent=self.get_agent()
        )

    def shortlist_applications(self):
        """Tool to analyze and shortlist applications using eligibility criteria"""
        try:
            applications = get_collection("applications").get()["metadatas"]

            response = self.gemini.generate_content(
                f"""You are reviewing student applications for university admission.

                Each application contains:
                - Student Name
                - Academic Scores
                - Extracurricular Activities
                - Special Notes (if any)

                Determine whether each applicant should be SHORTLISTED or REJECTED.
                Criteria:
                - High academic performance
                - Relevant extracurriculars
                - Compliance with policies

                Output JSON format:
                [
                  {{
                    "application_id": "...",
                    "student_name": "...",
                    "status": "shortlisted/rejected",
                    "reason": "..."
                  }},
                  ...
                ]

                Applications:
                {applications}
                """
            )

            return response.text

        except Exception as e:
            print(f"Error during shortlisting: {e}")
            return f"Shortlisting failed: {str(e)}"