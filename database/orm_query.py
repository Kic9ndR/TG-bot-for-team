from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import *


############################################## Работа с админами ##############################################

async def orm_add_admin(
    session: AsyncSession,
    user_id: int,
    name: str | None = None,
    username: str | None = None,
):
    query = select(AdminID).where(AdminID.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            AdminID(
                user_id=user_id, 
                name=name, 
                username=username, 
                )
        )
        await session.commit()


async def orm_get_admins(session: AsyncSession):
    query = select(AdminID)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_one_admin(session: AsyncSession, user_id):
    query = select(AdminID).where(AdminID.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()


############################################## Работа с вопросами ##############################################

async def orm_add_question(
    session: AsyncSession,
    contents: str,
    problem: str ,
    answer: str,
):
    query = select(FAQ)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            FAQ(
                contents=contents, 
                problem=problem, 
                answer=answer, 
            )
        )
        await session.commit()


async def orm_get_qq(session: AsyncSession):
    query = select(FAQ)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_one_ques(session: AsyncSession, contents: str):
    query = select(FAQ).where(FAQ.contents == contents)
    result = await session.execute(query)
    return result.scalar()