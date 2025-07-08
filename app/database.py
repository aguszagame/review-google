from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.models import Base
from app.config import settings
import logging

logger = logging.getLogger("db")
logger.setLevel(logging.INFO)

engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False,
)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Error en sesión DB: {e}")
        raise
    finally:
        await db.close()

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Base de datos inicializada correctamente.")
    except SQLAlchemyError as e:
        logger.error(f"Fallo al inicializar la base de datos: {e}")
        raise
