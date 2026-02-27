import asyncio
import httpx
import time
import uuid

BASE_URL = "http://127.0.0.1:8000/api/v1"

async def verify_achievements():
    print("🚀 Starting Achievement Engine Verification...")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Login
        print("🔑 Attempting login...")
        login_payload = {"email": "achiever@example.com", "password": "Password123!"}
        login_res = await client.post(f"{BASE_URL}/auth/login", json=login_payload)
        
        if login_res.status_code != 200:
            print("👤 User not found. Registering...")
            reg_payload = {
                "username": "achiever",
                "email": "achiever@example.com",
                "password": "Password123!"
            }
            reg_res = await client.post(f"{BASE_URL}/auth/register", json=reg_payload)
            if reg_res.status_code != 201:
                print(f"❌ Registration failed: {reg_res.json()}")
                return
            login_res = await client.post(f"{BASE_URL}/auth/login", json=login_payload)

        data = login_res.json()
        token = data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Get daily problem
        print("📅 Fetching daily problem...")
        problem_res = await client.get(f"{BASE_URL}/problems/daily", headers=headers)
        problem = problem_res.json()
        problem_id = problem["id"]

        # 3. Submit solution (triggers submission.accepted)
        print(f"📝 Submitting solution for '{problem['title']}'...")
        submit_res = await client.post(
            f"{BASE_URL}/submissions",
            headers=headers,
            json={
                "problem_id": problem_id,
                "code": "def solve(): pass",
                "language": "python"
            }
        )
        submission_id = submit_res.json()["id"]
        print(f"✅ Submitted! ID: {submission_id}")

        # 4. Play Rush (triggers rush.completed)
        print("🏃 Starting Rush session...")
        rush_start = await client.post(
            f"{BASE_URL}/rush/start", 
            headers=headers,
            json={"mode": "sudden_death"}
        )
        if rush_start.status_code != 200:
            print(f"❌ Rush start failed: {rush_start.json()}")
            return
            
        start_data = rush_start.json()
        session_id = start_data["session"]["id"]
        puzzle_id = start_data["first_puzzle"]["id"]

        # Submit 10 correct answers
        print("🎯 Solving 10 puzzles in Rush...")
        for i in range(10):
            await client.post(
                f"{BASE_URL}/rush/sessions/{session_id}/answer",
                headers=headers,
                json={
                    "puzzle_id": puzzle_id,
                    "user_answer": "O(log n)"
                }
            )
        
        # End session
        print("🏁 Ending Rush session...")
        await client.post(
            f"{BASE_URL}/rush/sessions/{session_id}/answer",
            headers=headers,
            json={
                "puzzle_id": puzzle_id,
                "user_answer": "wrong"
            }
        )

        # 5. Wait for background tasks (AI analysis and Achievement processing)
        print("⏳ Waiting for background processing (10s)...")
        await asyncio.sleep(10)

        # 6. Check achievements
        print("🏆 Checking earned achievements...")
        ach_res = await client.get(f"{BASE_URL}/achievements/me", headers=headers)
        achievements = ach_res.json()
        
        types = [a["achievement_type"] for a in achievements]
        print(f"Unlocked: {types}")

        if any(a in types for a in ["FIRST_SOLVER", "RUSH_10"]):
            print("✨ ACHIEVEMENT ENGINE VERIFIED! ✨")
        else:
            print("❌ No achievements found. Check Celery logs or conditions.")

if __name__ == "__main__":
    asyncio.run(verify_achievements())
