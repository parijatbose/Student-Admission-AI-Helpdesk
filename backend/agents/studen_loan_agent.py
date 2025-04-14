from crewai import Agent, Task
from langchain.tools import Tool
from backend.utils.gemini_client import get_gemini_client
from backend.data.database import get_collection


class StudentLoanAgent:
    def __init__(self):
        self.gemini = get_gemini_client()

    def process_loan_requests(self):
        try:
            loan_collection = get_collection("loan_requests")
            budget_collection = get_collection("university_budget")

            loan_requests = loan_collection.get(where={"status": "requested"})["metadatas"]
            budget_data = budget_collection.get(where={"type": "loan"})["metadatas"]

            if not budget_data:
                return "Loan budget information is missing."

            remaining_budget = budget_data[0].get("remaining_budget", 0)

            response = self.gemini.generate_content(
                f"""You are reviewing the following student loan requests for approval.
                University's total loan budget available: {remaining_budget}.

                Each loan request contains:
                - Student ID
                - Amount requested
                - Purpose
                - Evaluation notes (if any)

                Decide whether to APPROVE or REJECT each loan based on:
                1. Need and justification
                2. Requested amount vs. average tuition
                3. Total available budget

                Return a JSON list like:
                [
                  {{
                    "loan_id": "...",
                    "status": "approved/rejected",
                    "approved_amount": ...,
                    "reason": "..."
                  }},
                  ...
                ]

                Loan Requests:
                {loan_requests}
                """
            )

            return response.text
        except Exception as e:
            return f"Error during loan processing: {e}"

    def get_agent(self):
        return Agent(
            role="Student Loan Officer",
            goal="Evaluate and process student loan requests based on eligibility and budget constraints.",
            backstory="""You ensure students with genuine financial needs receive appropriate support. 
                          You evaluate merit, financial status, and remaining university loan budget.""",
            verbose=True,
            allow_delegation=False,
            tools=[
                Tool.from_function(
                    func=self.process_loan_requests,
                    name="ProcessLoanRequests",
                    description="Evaluates all loan requests and determines approval based on eligibility and budget."
                )
            ]
        )

    def create_loan_task(self):
        return Task(
            description="""Review all student loan requests and decide to approve or reject based on:
            - Need and justification
            - Budget availability
            - Request amount vs average tuition

            Return a JSON list of decisions with reasons.""",
            expected_output="List of approved/rejected loans with reasons and approved amounts.",
            agent=self.get_agent()
        )
