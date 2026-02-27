import asyncio
from sqlalchemy import select
from app.core.database import async_session_maker
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def ensure_dev_user():
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.username == "devuser"))
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                username="devuser",
                email="dev@kamicode.com",
                password_hash=pwd_context.hash("password"),
                classical_rating=1500,
                blitz_rating=1500,
                league_tier="gold"
            )
            session.add(user)
            await session.commit()
            print("✅ Created development user: devuser")
        else:
            print("⏩ Development user 'devuser' already exists.")

if __name__ == "__main__":
    asyncio.run(ensure_dev_user())
