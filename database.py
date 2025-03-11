from replit import db
from datetime import datetime, time
from models import PaymentStatus, StudentGrade
import json

def save_student(student_dict):
    """Save student data to Replit Database"""
    key = f"student_{student_dict['id']}"
    # Convert enum to string for storage
    student_dict['grade'] = student_dict['grade'].value
    db[key] = json.dumps(student_dict)

def get_student(student_id):
    """Get student data from Replit Database"""
    key = f"student_{student_id}"
    if key in db:
        student_data = json.loads(db[key])
        # Convert string back to enum
        student_data['grade'] = StudentGrade(student_data['grade'])
        return student_data
    return None

def get_all_students():
    """Get all students from Replit Database"""
    students = []
    for key in db.keys():
        if key.startswith('student_'):
            student_data = json.loads(db[key])
            student_data['grade'] = StudentGrade(student_data['grade'])
            students.append(student_data)
    return students

def save_lesson(lesson_dict):
    """Save lesson data to Replit Database"""
    key = f"lesson_{lesson_dict['id']}"
    # Convert datetime and enum to string for storage
    lesson_dict['date'] = lesson_dict['date'].isoformat()
    lesson_dict['time'] = lesson_dict['time'].isoformat()
    lesson_dict['payment_status'] = lesson_dict['payment_status'].value
    db[key] = json.dumps(lesson_dict)

def get_lesson(lesson_id):
    """Get lesson data from Replit Database"""
    key = f"lesson_{lesson_id}"
    if key in db:
        lesson_data = json.loads(db[key])
        # Convert strings back to datetime/enum
        lesson_data['date'] = datetime.fromisoformat(lesson_data['date'])
        lesson_data['time'] = datetime.fromisoformat(lesson_data['time']).time()
        lesson_data['payment_status'] = PaymentStatus(lesson_data['payment_status'])
        return lesson_data
    return None

def get_all_lessons():
    """Get all lessons from Replit Database"""
    lessons = []
    for key in db.keys():
        if key.startswith('lesson_'):
            lesson_data = json.loads(db[key])
            lesson_data['date'] = datetime.fromisoformat(lesson_data['date'])
            lesson_data['time'] = datetime.fromisoformat(lesson_data['time']).time()
            lesson_data['payment_status'] = PaymentStatus(lesson_data['payment_status'])
            lessons.append(lesson_data)
    return lessons

def get_student_lessons(student_id):
    """Get all lessons for a specific student"""
    lessons = []
    for key in db.keys():
        if key.startswith('lesson_'):
            lesson_data = json.loads(db[key])
            if lesson_data['student_id'] == student_id:
                lesson_data['date'] = datetime.fromisoformat(lesson_data['date'])
                lesson_data['time'] = datetime.fromisoformat(lesson_data['time']).time()
                lesson_data['payment_status'] = PaymentStatus(lesson_data['payment_status'])
                lessons.append(lesson_data)
    return lessons

def delete_student(student_id):
    """Delete student and their lessons"""
    # Delete student
    key = f"student_{student_id}"
    if key in db:
        del db[key]

    # Delete associated lessons
    for key in db.keys():
        if key.startswith('lesson_'):
            lesson_data = json.loads(db[key])
            if lesson_data['student_id'] == student_id:
                del db[key]

def delete_lesson(lesson_id):
    """Delete a lesson"""
    key = f"lesson_{lesson_id}"
    if key in db:
        del db[key]