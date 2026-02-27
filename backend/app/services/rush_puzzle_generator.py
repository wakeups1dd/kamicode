import json
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.services.ai_client import AIClient
from app.models.rush import RushPuzzle

class RushPuzzleGenerator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai = AIClient()

    async def generate_batch(self, count: int = 5, difficulty: int = 1) -> List[RushPuzzle]:
        """
        Generates a batch of Rush puzzles using AI.
        """
        system_prompt = (
            "You are an expert DSA educator. Generate a batch of quick-hit coding puzzles. "
            "Puzzles should be short and test core concepts (Time Complexity, Data Structures, Logic). "
            "Return a JSON object with a 'puzzles' list. "
            "Each puzzle must have: type (MCQ or FILL_BLANK), difficulty (1-5), "
            "content (object with 'question', 'options' for MCQ, 'answer', and 'code_snippet' if needed), "
            "explanation, and tags (list)."
        )
        
        user_prompt = f"Generate {count} unique puzzles of difficulty {difficulty}."
        
        print(f"🤖 Calling AI to generate {count} Rush puzzles...")
        
        # We need to handle the mock case in AIClient specifically for Rush if wanted,
        # but let's see what it returns first.
        json_str = await self.ai.generate_json(system_prompt, user_prompt)
        data = json.loads(json_str)
        
        generated_puzzles = []
        for p_data in data.get("puzzles", []):
            puzzle = RushPuzzle(
                type=p_data["type"],
                difficulty=p_data["difficulty"],
                content=p_data["content"],
                explanation=p_data.get("explanation"),
                tags=p_data.get("tags", [])
            )
            self.db.add(puzzle)
            generated_puzzles.append(puzzle)
        
        await self.db.commit()
        return generated_puzzles
