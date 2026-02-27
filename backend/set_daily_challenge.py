import asyncio
from datetime import date
from sqlalchemy import update
from app.core.database import async_session_maker
from app.models.problem import Problem

async def set_daily():
    today = date.today()
    async with async_session_maker() as session:
        # Set all previous daily_dates to None to be safe (or just leave them)
        # But let's just force Two Sum to today
        await session.execute(
            update(Problem)
            .where(Problem.slug == "two-sum")
            .values(daily_date=today)
        )
        await session.commit()
    print(f"✅ Set 'Two Sum' as daily challenge for {today}")

if __name__ == "__main__":
    asyncio.run(set_daily())
