import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from models import Base


load_dotenv()
login = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
port = os.getenv('DB_PORT')

engine = create_async_engine(f'postgresql+asyncpg://{login}:{password}@{host}:{port}/{db_name}')
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_schema() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
     asyncio.run(create_schema())
