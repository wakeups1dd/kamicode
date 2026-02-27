import openai
from app.core.config import get_settings

settings = get_settings()

class AIClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.base_url = settings.GEMINI_BASE_URL
        # Treat placeholder key as None
        if self.api_key and not self.api_key.startswith("sk-your-") and self.api_key != "YOUR_GEMINI_API_KEY":
            self.client = openai.AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        else:
            self.client = None

    async def generate_json(self, system_prompt: str, user_prompt: str, model: str = None):
        model = model or settings.AI_MODEL
        if not self.client:
            # Mock behavior if no key is provided
            print(f"⚠️ GEMINI_API_KEY not found. Returning mock for: {user_prompt[:30]}...")
            if "Rush" in system_prompt or "puzzle" in user_prompt.lower():
                return json.dumps({
                    "puzzles": [
                        {
                            "type": "MCQ",
                            "difficulty": 1,
                            "content": {
                                "question": "What is the time complexity of pushing to a stack?",
                                "options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"],
                                "answer": "O(1)"
                            },
                            "explanation": "Pushing to a stack is a constant time operation.",
                            "tags": ["stack", "basic"]
                        },
                        {
                            "type": "FILL_BLANK",
                            "difficulty": 1,
                            "content": {
                                "question": "The ______ data structure follows LIFO (Last-In-First-Out).",
                                "answer": "stack"
                            },
                            "explanation": "Stacks are LIFO structures.",
                            "tags": ["data-structures"]
                        }
                    ]
                })
            
            return json.dumps({
                "title": "Mock Inverse Array",
                "slug": f"mock-inverse-array-{int(time.time())}",
                "description": "Reverse the given array of integers.",
                "difficulty": "easy",
                "test_cases": {
                    "sample": [{"input": "1 2 3", "expected": "3 2 1"}],
                    "hidden": [{"input": "5 4\n3", "expected": "3\n4 5"}]
                },
                "constraints": "1 <= n <= 100",
                "tags": ["array", "basic"]
            })

        response = await self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        return response.choices[0].message.content

import json
import time
