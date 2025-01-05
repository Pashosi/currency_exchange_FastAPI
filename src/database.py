import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings

engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)

session = async_sessionmaker(bind=engine)


# Dependency для получения сессии
async def get_db():
    async with session() as sess:
        yield sess


# async def message_begin():
#     async with engine.connect() as connect:
#         res = await connect.execute(text("SELECT VERSION()"))
#         print(f'{res=}')
#
#
# asyncio.run(message_begin())
