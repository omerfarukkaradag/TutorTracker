import streamlit as st
import uuid
from datetime import datetime, time
from typing import List
from models import Student, Lesson, PaymentStatus

def initialize_session_state():
    if 'students' not in st.session_state:
        st.session_state.students = {}
    if 'lessons' not in st.session_state:
        st.session_state.lessons = {}

def add_student(name: str, email: str, phone: str, notes: str) -> Student:
    student = Student(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        phone=phone,
        notes=notes
    )
    st.session_state.students[student.id] = student
    return student

def add_lesson(
    student_id: str,
    date: datetime,
    time: time,
    duration: int,
    topics: str,
    payment_status: PaymentStatus,
    notes: str
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
    st.session_state.lessons[lesson.id] = lesson
    return lesson

def get_student_lessons(student_id: str) -> List[Lesson]:
    return [
        lesson for lesson in st.session_state.lessons.values()
        if lesson.student_id == student_id
    ]

def format_time(t: time) -> str:
    return t.strftime("%I:%M %p")