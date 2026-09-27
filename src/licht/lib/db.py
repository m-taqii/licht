from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from licht.lib.config import get_settings

class Base(DeclarativeBase):
    pass

settings = get_settings()
BaseModel = Base()

database_url = settings.database_url
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql://") and not database_url.startswith("postgresql+psycopg://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

connect_args = {}
pool_kwargs = {}
if "sqlite" in database_url:
    if not database_url.startswith("sqlite+aiosqlite://"):
        database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    connect_args = {"check_same_thread": False}
else:
    pool_kwargs = {"pool_size": 10, "max_overflow": 20}

engine = create_async_engine(
    database_url,
    echo=settings.dev_mode,
    connect_args=connect_args,
    pool_pre_ping=True,
    **pool_kwargs
)

SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def init_db():
    """Create all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def close_db():
    """Dispose of the connection pool."""
    await engine.dispose()

async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise