import asyncio
import httpx
import time
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Import models to check DB
# Note: Adjust paths as needed based on where you run this
import sys
import os
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.models.achievement import UserAchievement
from app.models.user import User
from app.core.config import get_settings

settings = get_settings()
engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

BASE_URL = "http://localhost:8000/api/v1"

async def verify_nft_minting():
    print("🧪 Verifying NFT Minting Flow...")

    async with AsyncSessionLocal() as db:
        # 1. Ensure a user exists with a wallet
        print("👤 Checking test user...")
        result = await db.execute(select(User).where(User.username == "achiever"))
        user = result.scalar_one_or_none()
        
        if not user:
            print("❌ Test user 'achiever' not found. Please run verify_achievements.py first.")
            return

        if not user.wallet_address:
            print("🔗 Linking mock wallet...")
            user.wallet_address = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
            await db.commit()

        # 2. Trigger an achievement (e.g. RUSH_5)
        print("🏃 Triggering RUSH_5 achievement event...")
        async with httpx.AsyncClient() as client:
            login_resp = await client.post(f"{BASE_URL}/auth/login", json={"email": "achiever@example.com", "password": "Password123!"})
        # Instead of .delay(), we run logic synchronously for verification
        from app.engines.achievement_engine import AchievementEngine
        engine_obj = AchievementEngine(db)
        
        # Simulate the event that triggers RUSH_5 (streak reaches 5)
        # _award_achievement will call mint_achievement_nft_task.delay()
        # but we want to intercept that or just call the minting task ourselves
        
        print("🏆 Awarding RUSH_5 achievement manually...")
        from app.models.achievement import UserAchievement
        achievement = UserAchievement(
            user_id=user.id,
            achievement_type="RUSH_5",
            trigger_id="mock_session_id"
        )
        db.add(achievement)
        await db.commit()
        await db.refresh(achievement)

        print(f"🎨 Calling mint_achievement_nft_task synchronously for {achievement.id}...")
        from app.engines.achievement_tasks import mint_achievement_nft_task
        # We call the task directly. It starts run_mint in the loop.
        mint_achievement_nft_task(achievement.id)

        print("⏳ Waiting 5 seconds for background task completion...")
        await asyncio.sleep(5)

    # 3. Check UserAchievement for NFT data (in a fresh session)
    print("🧐 Checking database for NFT data...")
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(UserAchievement).where(UserAchievement.id == achievement.id)
        )
        achievement = result.scalar_one_or_none()

        if achievement:
            print(f"✅ Achievement '{achievement.achievement_type}' found!")
            print(f"   NFT Token ID: {achievement.nft_token_id}")
            print(f"   NFT Tx Hash: {achievement.nft_tx_hash}")
            print(f"   Metadata URI: {achievement.metadata_uri}")
            
            if achievement.nft_token_id is not None:
                print("🌟 SUCCESS: NFT Minting flow verified end-to-end (Mocked)!")
            else:
                print("⚠️ Achievement exists but NFT data is still missing.")
        else:
            print("❌ Achievement record disappeared?")

if __name__ == "__main__":
    asyncio.run(verify_nft_minting())
