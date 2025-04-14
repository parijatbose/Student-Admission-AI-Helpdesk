from crewai import Agent, Task
from langchain.tools import Tool
from backend.utils.gemini_client import get_gemini_client
from backend.data.database import get_collection


class AdmissionOfficerAgent:
    def __init__(self):
        self.gemini = get_gemini_client()

    def get_agent(self):
        """Return the CrewAI agent responsible for screening admission applications."""
        return Agent(
            role="Admission Officer",
            goal="Screen applications for eligibility based on academic criteria and application completeness.",
            backstory="""You are an experienced admissions officer responsible for carefully screening student applications.
            You review academic credentials, check form completeness, and flag any issues before shortlisting.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                Tool.from_function(
                    func=self.screen_applications,
                    name="ScreenApplications",
                    description="Screen applications for eligibility based on academic merit and application completeness."
                )
            ]
        )

    def create_screening_task(self):
        """Create a task to screen submitted admission applications."""
        return Task(
            description="""Screen all student applications and evaluate:
            - Academic performance
            - Completeness of the form
            - Presence of mandatory fields and documents

            Flag applications with missing info or weak credentials and recommend eligible ones.
            """,
            expected_output="A JSON list of screened applications with status: eligible/ineligible and reasoning.",
            agent=self.get_agent()
        )

    def screen_applications(self):
        """Tool logic to screen applications for admission eligibility."""
        try:
            application_collection = get_collection("applications")
            applications = application_collection.get(where={"status": "submitted"})["metadatas"]

            if not applications:
                return "No applications to screen."

            response = self.gemini.generate_content(
                f"""You are screening the following student applications:

                Each application includes:
                - Student name
                - Academic scores
                - List of submitted documents

                Evaluate each application and return a JSON list like:
                [
                  {{
                    "application_id": "...",
                    "student_name": "...",
                    "status": "eligible/ineligible",
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
            print(f"Error screening applications: {e}")
            return f"Error: {str(e)}"
