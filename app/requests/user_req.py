from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select


class UserRequests:

    async def chek_user(tg_id):
        async with async_session() as session:
            user_query = await session.scalar(select(User).where(User.tg_id == tg_id))
            if not user_query:
                return False
            
            return True

    async def save_responces(data, tg_id, username):
        async with async_session() as session:
            try:
                session.add(User(tg_id=tg_id, username=username, data=data))
                await session.commit()
                return True
            except Exception as exxit:
                print(exxit)
                return False    

    # async def save_user(tg_id, username):
    #     async with async_session() as session:
    #         session.add(User(tg_id=tg_id, username=username))
    #         await session.commit()


