from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool, StaticPool
from app.core.config import settings

# Create database engine
kwargs = {}
if "sqlite" in settings.DATABASE_URL:
    # SQLite requires StaticPool for in-memory or file-based databases
    kwargs["connect_args"] = {"check_same_thread": False}
    kwargs["poolclass"] = StaticPool
elif settings.ENVIRONMENT == "production":
    kwargs["poolclass"] = NullPool

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    **kwargs
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()
