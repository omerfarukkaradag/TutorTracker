import streamlit as st
import uuid
from datetime import datetime, time
from typing import List
from models import Student, Lesson, PaymentStatus, StudentGrade
from database import Session, Student as DBStudent, Lesson as DBLesson

def initialize_session_state():
    if 'students' not in st.session_state:
        st.session_state.students = {}
    if 'lessons' not in st.session_state:
        st.session_state.lessons = {}

    # Veritabanından verileri yükle
    load_data_from_db()

def load_data_from_db():
    session = Session()
    try:
        # Öğrencileri yükle
        students = session.query(DBStudent).all()
        st.session_state.students = {
            student.id: Student(
                id=student.id,
                name=student.name,
                phone=student.phone,
                grade=student.grade,
                notes=student.notes
            ) for student in students
        }

        # Dersleri yükle
        lessons = session.query(DBLesson).all()
        st.session_state.lessons = {
            lesson.id: Lesson(
                id=lesson.id,
                student_id=lesson.student_id,
                date=lesson.date,
                time=lesson.time,
                duration=lesson.duration,
                topics=lesson.topics,
                payment_status=lesson.payment_status,
                notes=lesson.notes,
                attendance=lesson.attendance
            ) for lesson in lessons
        }
    finally:
        session.close()

def add_student(name: str, phone: str, grade: StudentGrade, notes: str) -> Student:
    student = Student(
        id=str(uuid.uuid4()),
        name=name,
        phone=phone,
        grade=grade,
        notes=notes
    )

    # Veritabanına kaydet
    session = Session()
    try:
        db_student = DBStudent(
            id=student.id,
            name=student.name,
            phone=student.phone,
            grade=student.grade,
            notes=student.notes
        )
        session.add(db_student)
        session.commit()

        # Session state'i güncelle
        st.session_state.students[student.id] = student
    finally:
        session.close()

    return student

def add_lesson(
    student_id: str,
    date: datetime,
    time: time,
    duration: int,
    topics: str = "",
    payment_status: PaymentStatus = PaymentStatus.UNPAID,
    notes: str = ""
) -> Lesson:
    lesson = Lesson(
        id=str(uuid.uuid4()),
        student_id=student_id,
        date=date,
        time=time,
        duration=duration,
        topics=topics,
        payment_status=payment_status,
        notes=notes
    )

    # Veritabanına kaydet
    session = Session()
    try:
        db_lesson = DBLesson(
            id=lesson.id,
            student_id=lesson.student_id,
            date=lesson.date,
            time=lesson.time,
            duration=lesson.duration,
            topics=lesson.topics,
            payment_status=lesson.payment_status,
            notes=lesson.notes
        )
        session.add(db_lesson)
        session.commit()

        # Session state'i güncelle
        st.session_state.lessons[lesson.id] = lesson
    finally:
        session.close()

    return lesson

def get_student_lessons(student_id: str) -> List[Lesson]:
    session = Session()
    try:
        db_lessons = session.query(DBLesson).filter(DBLesson.student_id == student_id).all()
        return [
            Lesson(
                id=lesson.id,
                student_id=lesson.student_id,
                date=lesson.date,
                time=lesson.time,
                duration=lesson.duration,
                topics=lesson.topics,
                payment_status=lesson.payment_status,
                notes=lesson.notes,
                attendance=lesson.attendance
            ) for lesson in db_lessons
        ]
    finally:
        session.close()

def format_time(t: time) -> str:
    return t.strftime("%H:%M")