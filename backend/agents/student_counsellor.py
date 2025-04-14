from crewai import Agent, Task
from langchain.tools import Tool
from backend.utils.gemini_client import get_gemini_client
from backend.data.database import get_collection


class StudentCounsellorAgent:
    def __init__(self):
        self.gemini = get_gemini_client()

    def get_agent(self):
        """Return the CrewAI agent responsible for student communication and guidance."""
        return Agent(
            role="Student Counsellor",
            goal="Provide students with updates and support regarding their admission process.",
            backstory="""You are a compassionate and helpful counsellor guiding students through their admission process.
            You provide timely updates, explain admission statuses, and ensure students feel supported and informed.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                Tool.from_function(
                    func=self.communicate_with_student,
                    name="CommunicateWithStudent",
                    description="Sends admission status updates and helpful information to a student."
                )
            ]
        )

    def create_communication_task(self, student_id, admission_stage):
        """Create a task to send a personalized communication message to a student"""
        return Task(
            description=f"""Send an update to student with ID {student_id} about their current admission stage: '{admission_stage}'.

            Ensure the message is friendly, clear, and informative. Include:
            - A brief explanation of the current stage
            - Any required actions from the student
            - Contact info for further help
            """,
            expected_output="A well-written message ready to send to the student.",
            agent=self.get_agent()
        )

    def communicate_with_student(self, student_id: str, admission_stage: str):
        """Tool to send personalized admission updates to a student"""
        try:
            student_collection = get_collection("students")
            student_data = student_collection.get(ids=[student_id])["metadatas"][0]

            response = self.gemini.generate_content(
                f"""Write a message for student {student_data['name']} (ID: {student_id}).

                Their current admission stage is: {admission_stage}.

                Make the message:
                - Friendly and supportive
                - Clear about the current step in the process
                - Include any actions the student needs to take
                - Mention they can contact the counsellor if they have questions
                """
            )

            return response.text
        except Exception as e:
            print(f"Error communicating with student: {e}")
            return f"Error generating message: {str(e)}"
