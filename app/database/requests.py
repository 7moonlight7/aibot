from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User, async_session
from datetime import datetime
from sqlalchemy import select, update, delete, desc


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def save_image_to_db(tg_id: int, image_data: bytes, promt: str):
    async with async_session() as session:
        user_image = User(tg_id=tg_id, image=image_data, created_at=datetime.utcnow(), promt = promt)

        session.add(user_image)

        await session.commit()

async def get_user_history(tg_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(User).where(User.tg_id == tg_id).order_by(User.created_at.desc()))
        user_images = result.scalars().all()
        return user_images