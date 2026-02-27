"""
KamiCode — Achievement Tasks

Celery tasks for background achievement processing.
"""

import asyncio
from sqlalchemy import select
from app.core.celery_app import celery_app
from app.core.database import async_session_maker
from app.engines.achievement_engine import AchievementEngine
from app.models.achievement import UserAchievement
from app.models.user import User
from app.services.ipfs_service import IPFSService
from app.services.nft_minting_service import NFTMintingService

@celery_app.task(name="app.engines.achievement_tasks.process_achievement_event_task")
def process_achievement_event_task(event_type: str, event_data: dict):
    """
    Background task to process achievement events.
    """
    async def run_process():
        async with async_session_maker() as db:
            engine = AchievementEngine(db)
            await engine.process_event(event_type, event_data)

    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(run_process())
    else:
        loop.run_until_complete(run_process())

@celery_app.task(name="app.engines.achievement_tasks.mint_achievement_nft_task")
def mint_achievement_nft_task(user_achievement_id: str):
    """
    Background task to pin metadata and mint an NFT for an achievement.
    """
    async def run_mint():
        try:
            async with async_session_maker() as db:
                # 1. Fetch data
                stmt = select(UserAchievement).where(UserAchievement.id == user_achievement_id)
                result = await db.execute(stmt)
                achievement = result.scalar_one_or_none()
                if not achievement:
                    print(f"❌ Achievement {user_achievement_id} not found.")
                    return

                user = await db.get(User, achievement.user_id)
                if not user or not user.wallet_address:
                    print(f"⚠️ Skipping mint: User {achievement.user_id} has no wallet.")
                    return

                # 2. IPFS Metadata
                print(f"📦 Pinning metadata for {achievement.achievement_type}...")
                ipfs = IPFSService()
                metadata = ipfs.get_achievement_metadata(
                    achievement_type=achievement.achievement_type,
                    username=user.username,
                    description=f"Awarded for exceptional performance in {achievement.achievement_type}."
                )
                metadata_uri = await ipfs.pin_json(metadata)

                # 3. Mint NFT
                print(f"🎨 Minting NFT to {user.wallet_address}...")
                nft_service = NFTMintingService()
                token_id, tx_hash = await nft_service.mint_achievement_nft(
                    to_address=user.wallet_address,
                    achievement_type=achievement.achievement_type,
                    metadata_uri=metadata_uri
                )

                if token_id is not None:
                    achievement.nft_token_id = token_id
                    achievement.nft_tx_hash = tx_hash
                    achievement.metadata_uri = metadata_uri
                    await db.commit()
                    print(f"✅ NFT Minted! ID: {token_id}, Tx: {tx_hash}")
                else:
                    print(f"❌ NFT Minting failed (returned None).")
        except Exception as e:
            print(f"💥 Critical error in mint_achievement_nft_task: {e}")
            import traceback
            traceback.print_exc()

    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(run_mint())
    else:
        loop.run_until_complete(run_mint())
