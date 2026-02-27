import json
from datetime import date, timedelta
from typing import Optional
from app.services.ai_client import AIClient
from app.services.problem_service import ProblemService
from app.schemas.problem import ProblemCreate, ProblemTestCases, TestCase

class ProblemGenerator:
    def __init__(self, db):
        self.ai = AIClient()
        self.problem_service = ProblemService(db)

    async def generate_daily_problem(self, topic: str = None, difficulty: str = "easy") -> Optional[any]:
        system_prompt = (
            "You are an expert competitive programming problem setter. "
            "Generate a unique coding problem in JSON format. "
            "The JSON must have: title, slug, description (markdown), difficulty, "
            "test_cases (object with 'sample' and 'hidden' lists, each containing 'input' and 'expected'), "
            "constraints (markdown), and tags (list of strings)."
        )
        
        user_prompt = f"Create a {difficulty} problem"
        if topic:
            user_prompt += f" about {topic}"
        user_prompt += ". Ensure test cases are robust and handle edge cases."

        print(f"🤖 Calling AI to generate {difficulty} problem...")
        json_str = await self.ai.generate_json(system_prompt, user_prompt)
        data = json.loads(json_str)

        # Convert to ProblemCreate schema
        # (Assuming the AI follows the JSON structure closely)
        problem_data = ProblemCreate(
            title=data["title"],
            slug=data["slug"],
            description=data["description"],
            difficulty=data["difficulty"].lower(),
            test_cases=ProblemTestCases(
                sample=[TestCase(**tc) for tc in data["test_cases"]["sample"]],
                hidden=[TestCase(**tc) for tc in data["test_cases"]["hidden"]]
            ),
            constraints=data.get("constraints"),
            tags=data.get("tags", [])
        )

        return await self.problem_service.create_problem(problem_data)
