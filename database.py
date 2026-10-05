import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Database location
DATABASE_URL = "sqlite:///data/students.db"

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)

# Base class
Base = declarative_base()


# Student table
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    section = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)


# Attendance table
class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    total_classes = Column(Integer, default=0)
    attended_classes = Column(Integer, default=0)


# Marks table
class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    roll_number = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    marks = Column(Float, default=0)


# Create all tables
Base.metadata.create_all(engine)

# Create database session
SessionLocal = sessionmaker(bind=engine)


def get_session():
    return SessionLocal()