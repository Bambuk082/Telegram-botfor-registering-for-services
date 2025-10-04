from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs, create_async_engine


DB_URL = 'sqlite+aiosqlite:///db.sqlite3'
engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass




async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)