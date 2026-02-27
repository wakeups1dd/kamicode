import requests
import uuid
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def test_rush_flow():
    print("\n🚀 Starting Rush Mode Verification...")
    
    # 1. Setup User
    username = f"rush_runner_{uuid.uuid4().hex[:6]}"
    reg_data = {"username": username, "email": f"{username}@example.com", "password": "Password123!"}
    resp = requests.post(f"{BASE_URL}/auth/register", json=reg_data)
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Start Rush Session
    start_data = {"mode": "sudden_death"} # 1 life
    resp = requests.post(f"{BASE_URL}/rush/start", json=start_data, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    session_id = data["session"]["id"]
    first_puzzle = data["first_puzzle"]
    print(f"🎮 Session Started: {session_id} (Mode: {data['session']['mode']})")
    print(f"🧩 First Puzzle: {first_puzzle['content']['question']}")
    
    # 3. Submit Correct Answer
    correct_answer = first_puzzle["content"]["answer"]
    ans_data = {"puzzle_id": first_puzzle["id"], "user_answer": correct_answer}
    resp = requests.post(f"{BASE_URL}/rush/sessions/{session_id}/answer", json=ans_data, headers=headers)
    assert resp.status_code == 200
    res = resp.json()
    print(f"✅ Correct! Score: {res['current_score']}, Streak: {res['current_streak']}")
    assert res["is_correct"] is True
    
    next_puzzle = res["next_puzzle"]
    
    # 4. Submit Wrong Answer to end Sudden Death
    ans_data = {"puzzle_id": next_puzzle["id"], "user_answer": "Wrong Answer"}
    resp = requests.post(f"{BASE_URL}/rush/sessions/{session_id}/answer", json=ans_data, headers=headers)
    assert resp.status_code == 200
    res = resp.json()
    print(f"❌ Wrong! lives_remaining: {res['lives_remaining']}, status: {res['status']}")
    
    # In sudden_death, status should be 'completed'
    assert res["status"] == "completed"
    assert res["lives_remaining"] == 0
    
    # 5. Check final session details
    resp = requests.get(f"{BASE_URL}/rush/sessions/{session_id}", headers=headers)
    session = resp.json()
    print(f"🏁 Final Session Rating Change: {session['rating_change']}")
    assert session["status"] == "completed"
    
    print("✨ RUSH ENGINE VERIFIED. ✨")

if __name__ == "__main__":
    test_rush_flow()
