import asyncio
from datetime import date
from sqlalchemy import select
from app.core.database import async_session_maker
from app.models.problem import Problem

async def seed_problems():
    print("🌱 Seeding problems...")
    
    problems = [
        {
            "title": "Two Sum",
            "slug": "two-sum",
            "description": (
                "Given an array of integers `nums` and an integer `target`, return indices of the "
                "two numbers such that they add up to `target`.\n\n"
                "You may assume that each input would have exactly one solution, and you may "
                "not use the same element twice."
            ),
            "difficulty": "easy",
            "test_cases": {
                "sample": [
                    {"input": "2 7 11 15\n9", "expected": "0 1"},
                    {"input": "3 2 4\n6", "expected": "1 2"}
                ],
                "hidden": [
                    {"input": "3 3\n6", "expected": "0 1"}
                ]
            },
            "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9",
            "tags": ["array", "hash-table"],
            "daily_date": date.today()
        },
        {
            "title": "FizzBuzz",
            "slug": "fizzbuzz",
            "description": (
                "Given an integer `n`, return a string array answer (1-indexed) where:\n"
                "- `answer[i] == 'FizzBuzz'` if `i` is divisible by 3 and 5.\n"
                "- `answer[i] == 'Fizz'` if `i` is divisible by 3.\n"
                "- `answer[i] == 'Buzz'` if `i` is divisible by 5.\n"
                "- `answer[i] == i` (as a string) if none of the above conditions are true."
            ),
            "difficulty": "easy",
            "test_cases": {
                "sample": [
                    {"input": "3", "expected": "1\n2\nFizz"},
                    {"input": "5", "expected": "1\n2\nFizz\n4\nBuzz"}
                ],
                "hidden": [
                    {"input": "15", "expected": "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"}
                ]
            },
            "constraints": "1 <= n <= 10^4",
            "tags": ["basic", "math"],
            "daily_date": None
        }
    ]

    async with async_session_maker() as session:
        for p_data in problems:
            # Check if exists
            result = await session.execute(select(Problem).where(Problem.slug == p_data["slug"]))
            if result.scalar_one_or_none():
                print(f"⏩ Problem '{p_data['title']}' already exists, skipping...")
                continue
                
            new_problem = Problem(**p_data)
            session.add(new_problem)
            print(f"✅ Added '{p_data['title']}'")
            
        await session.commit()
    
    print("✨ Seeding complete!")

if __name__ == "__main__":
    asyncio.run(seed_problems())
