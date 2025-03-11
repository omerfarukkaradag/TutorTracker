from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Optional
from enum import Enum

class PaymentStatus(Enum):
    PAID = "Ödendi"
    UNPAID = "Ödenmedi"

class StudentGrade(Enum):
    NINTH = "9. Sınıf"
    TENTH = "10. Sınıf"
    ELEVENTH = "11. Sınıf"
    TWELFTH = "12. Sınıf"
    GRADUATE = "Mezun"

@dataclass
class Student:
    id: str
    name: str
    phone: str
    grade: StudentGrade
    notes: str = ""

@dataclass
class Lesson:
    id: str
    student_id: str
    date: datetime
    time: time
    duration: int  # in minutes
    topics: str
    payment_status: PaymentStatus
    notes: str = ""
    attendance: bool = False