from sqlalchemy import create_engine, Column, String, Integer, DateTime, Time, Boolean, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime, time
from models import PaymentStatus, StudentGrade

# PostgreSQL veritabanı bağlantısı
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class Student(Base):
    __tablename__ = 'students'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    grade = Column(Enum(StudentGrade), nullable=False)
    notes = Column(String)

    lessons = relationship("Lesson", back_populates="student", cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = 'lessons'

    id = Column(String, primary_key=True)
    student_id = Column(String, ForeignKey('students.id'), nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)
    topics = Column(String)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.UNPAID)
    notes = Column(String)
    attendance = Column(Boolean, default=False)

    student = relationship("Student", back_populates="lessons")

# Veritabanı tablolarını oluştur
Base.metadata.create_all(engine)