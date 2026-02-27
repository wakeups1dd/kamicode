import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from app.models.ai_analysis import AIAnalysis
from app.models.submission import Submission
from app.models.problem import Problem
from app.services.ai_client import AIClient
from app.engines.achievement_tasks import process_achievement_event_task

class AIAnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.ai_client = AIClient()

    async def analyze_submission(self, submission_id: str) -> Optional[AIAnalysis]:
        """
        Analyze a submission using AI for complexity and quality.
        """
        # 1. Fetch submission and problem details
        result = await self.db.execute(
            select(Submission, Problem)
            .join(Problem, Submission.problem_id == Problem.id)
            .where(Submission.id == submission_id)
        )
        data = result.one_or_none()
        if not data:
            return None
        
        submission, problem = data

        if submission.verdict != "accepted":
            print(f"⏩ Skipping analysis for non-accepted submission {submission_id}")
            return None

        # 2. Prepare AI Prompt
        system_prompt = (
            "You are a Senior Software Engineer and Competitive Programmer. "
            "Analyze the provided code for time/space complexity and code quality. "
            "Return a JSON object with: time_complexity, space_complexity, approach_name, quality_score (0-100), and feedback."
        )
        
        user_prompt = f"""
Problem: {problem.title}
Description: {problem.description}
Constraints: {problem.constraints}

User Code ({submission.language}):
{submission.code}

Execution Context:
Runtime: {submission.runtime_ms}ms
"""

        # 3. Call AI (with fallback handled in AIClient)
        print(f"🤖 Analyzing submission {submission_id}...")
        
        # We manually handle the mock logic here if we want more specific mock data for analysis
        if not self.ai_client.client:
            print("⚠️ Using mock analysis result...")
            analysis_data = {
                "time_complexity": "O(n)",
                "space_complexity": "O(n)",
                "approach_name": "Efficient Hash Table",
                "quality_score": 95,
                "feedback": "Excellent use of a hash map to achieve linear time complexity. The code is clean and follows best practices."
            }
        else:
            json_str = await self.ai_client.generate_json(system_prompt, user_prompt)
            analysis_data = json.loads(json_str)

        # 4. Calculate Percentile Rank (Simple mock logic for now, or real if we have enough data)
        # For now, let's just use a random rank or 0.5 to keep it simple, 
        # but the plan mentions calculating it among accepted solutions.
        percentile = await self.calculate_percentile(problem.id, submission.runtime_ms)

        # 5. Save to DB
        analysis = AIAnalysis(
            submission_id=submission_id,
            time_complexity=analysis_data.get("time_complexity"),
            space_complexity=analysis_data.get("space_complexity"),
            approach_name=analysis_data.get("approach_name"),
            quality_score=analysis_data.get("quality_score"),
            feedback=analysis_data.get("feedback"),
            percentile_rank=percentile,
            model_used="Mock" if not self.ai_client.client else "gpt-4o-mini"
        )
        
        self.db.add(analysis)
        
        # Link submission to analysis
        submission.ai_analysis_id = analysis.id
        
        await self.db.commit()
        await self.db.refresh(analysis)
        
        # 6. Trigger Achievement: submission.analyzed
        try:
            process_achievement_event_task.delay("submission.analyzed", {
                "user_id": submission.user_id,
                "submission_id": submission_id,
                "analysis_id": analysis.id,
                "quality_score": analysis.quality_score,
                "percentile": analysis.percentile_rank
            })
        except Exception as e:
            print(f"⚠️ Failed to enqueue analysis achievement: {e}")
        
        return analysis

    async def calculate_percentile(self, problem_id: str, runtime_ms: int) -> float:
        """
        Calculate the runtime percentile for an accepted solution.
        """
        # Count total accepted submissions for this problem
        total_result = await self.db.execute(
            select(func.count(Submission.id))
            .where(Submission.problem_id == problem_id, Submission.verdict == "accepted")
        )
        total_count = total_result.scalar() or 0
        
        if total_count <= 1:
            return 100.0  # Top 100% if only one submission
            
        # Count submissions with strictly greater runtime
        slower_result = await self.db.execute(
            select(func.count(Submission.id))
            .where(
                Submission.problem_id == problem_id, 
                Submission.verdict == "accepted",
                Submission.runtime_ms > runtime_ms
            )
        )
        slower_count = slower_result.scalar() or 0
        
        # Percentile = (slower_count / (total_count - 1)) * 100
        return (slower_count / total_count) * 100.0

    async def get_analysis_by_submission(self, submission_id: str) -> Optional[AIAnalysis]:
        result = await self.db.execute(select(AIAnalysis).where(AIAnalysis.submission_id == submission_id))
        return result.scalar_one_or_none()
