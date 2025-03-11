import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import json

# Assuming PaymentStatus is defined elsewhere in the project
class PaymentStatus:
    PAID = "Paid"
    PENDING = "Pending"
    OVERDUE = "Overdue"


def render_calendar_view():
    st.header("Ders Takvimi")

    # Prepare calendar events
    events = []
    for lesson in st.session_state.lessons.values():
        student = st.session_state.students.get(lesson.student_id)
        if not student:
            continue

        start_time = datetime.combine(lesson.date, lesson.time)
        end_time = start_time + timedelta(minutes=lesson.duration)

        event = {
            'id': lesson.id,
            'title': f"{student.name} - {lesson.topics}",
            'start': start_time.isoformat(),
            'end': end_time.isoformat(),
            'backgroundColor': {
                PaymentStatus.PAID.value: '#28a745',
                PaymentStatus.PENDING.value: '#ffc107',
                PaymentStatus.OVERDUE.value: '#dc3545'
            }[lesson.payment_status.value]
        }
        events.append(event)

    # Calendar configuration
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "initialView": "timeGridWeek",
        "slotMinTime": "06:00:00",
        "slotMaxTime": "22:00:00",
        "height": 600,
        "locale": "tr"
    }

    # Render calendar
    calendar(events=events, options=calendar_options)