from sqlalchemy import Column, Integer, String, Boolean, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DB_BACKEND, SQLITE_URL, POSTGRES_URL

Base = declarative_base()

def get_engine():
    return create_engine(SQLITE_URL if DB_BACKEND == "sqlite" else POSTGRES_URL)

class ICD10Code(Base):
    __tablename__ = "icd10_codes"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), unique=True, index=True)
    year = Column(Integer, index=True)

    order_number = Column(Integer)
    is_billable = Column(Boolean)
    short_description = Column(String(255))
    long_description = Column(Text)
    source = Column(String(50))

def init_db():
    engine = get_engine()
    Base.metadata.create_all(engine)
    return engine

SessionLocal = sessionmaker(bind=get_engine())

