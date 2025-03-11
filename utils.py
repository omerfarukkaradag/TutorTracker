import streamlit as st
import uuid
from datetime import datetime, time
from typing import List
from models import Student, Lesson, PaymentStatus, StudentGrade
import database as db

def initialize_session_state():
    if 'students' not in st.session_state:
        st.session_state.students = {}
    if 'lessons' not in st.session_state:
        st.session_state.lessons = {}

    # Veritabanından verileri yükle
    load_data_from_db()

def load_data_from_db():
    # Öğrencileri yükle
    students = db.get_all_students()
    st.session_state.students = {
        student['id']: Student(
            id=student['id'],
            name=student['name'],
            phone=student['phone'],
            grade=student['grade'],
            notes=student['notes']
        ) for student in students
    }

    # Dersleri yükle
    lessons = db.get_all_lessons()
    st.session_state.lessons = {
        lesson['id']: Lesson(
            id=lesson['id'],
            student_id=lesson['student_id'],
            date=lesson['date'],
            time=lesson['time'],
            duration=lesson['duration'],
            topics=lesson['topics'],
            payment_status=lesson['payment_status'],
            notes=lesson['notes'],
            attendance=lesson['attendance']
        ) for lesson in lessons
    }

def add_student(name: str, phone: str, grade: StudentGrade, notes: str) -> Student:
    student = Student(
        id=str(uuid.uuid4()),
        name=name,
        phone=phone,
        grade=grade,
        notes=notes
    )

    # Veritabanına kaydet
    db.save_student(student.__dict__)

    # Session state'i güncelle
    st.session_state.students[student.id] = student
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
    db.save_lesson(lesson.__dict__)

    # Session state'i güncelle
    st.session_state.lessons[lesson.id] = lesson
    return lesson

def get_student_lessons(student_id: str) -> List[Lesson]:
    lessons_data = db.get_student_lessons(student_id)
    return [
        Lesson(
            id=lesson['id'],
            student_id=lesson['student_id'],
            date=lesson['date'],
            time=lesson['time'],
            duration=lesson['duration'],
            topics=lesson['topics'],
            payment_status=lesson['payment_status'],
            notes=lesson['notes'],
            attendance=lesson['attendance']
        ) for lesson in lessons_data
    ]

def delete_student(student_id: str):
    # Veritabanından sil
    db.delete_student(student_id)
    # Session state'den sil
    if student_id in st.session_state.students:
        del st.session_state.students[student_id]

def delete_lesson(lesson_id: str):
    # Veritabanından sil
    db.delete_lesson(lesson_id)
    # Session state'den sil
    if lesson_id in st.session_state.lessons:
        del st.session_state.lessons[lesson_id]

def format_time(t: time) -> str:
    return t.strftime("%H:%M")