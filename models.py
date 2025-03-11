from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Optional
from enum import Enum

class PaymentStatus(Enum):
    PAID = "Paid"
    PENDING = "Pending"
    OVERDUE = "Overdue"

@dataclass
class Student:
    id: str
    name: str
    email: str
    phone: str
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
