import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

default_db_url = "postgresql+asyncpg://revai:password@postgres:5432/revai"
database_url = os.getenv("DATABASE_URL", default_db_url)
supabase_direct_url = os.getenv("SUPABASE_DIRECT_URL", "")

# Prefer Supabase direct URL only when it has a real password.
if supabase_direct_url and "[YOUR-PASSWORD]" not in supabase_direct_url:
    database_url = supabase_direct_url

# If using psycopg2 driver in URL, update to asyncpg
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(database_url, echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
