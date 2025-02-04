from sqlalchemy import create_engine, Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the base class for our ORM models.
Base = declarative_base()

class StockData(Base):
    """
    The StockData model represents a single row of stock information.
    All columns from the CSV (including static asset info and daily price data)
    are stored in this table.
    """
    __tablename__ = 'stock_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)                  # Asset name (e.g., "Amazon Com")
    asof = Column(Date, index=True)                    # Date of the record
    volume = Column(Integer)                           # Trading volume
    close_usd = Column(Float)                          # Closing price in USD
    sector_level1 = Column(String, index=True)         # Primary sector classification
    sector_level2 = Column(String, index=True)         # Secondary sector classification

# Function to create an SQLAlchemy engine. Here we use SQLite.
def get_engine(db_url='sqlite:///market_data.db'):
    return create_engine(db_url, echo=False)

# Function to create database tables (if they don't already exist).
def create_tables(engine):
    Base.metadata.create_all(engine)

# Session maker for database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
