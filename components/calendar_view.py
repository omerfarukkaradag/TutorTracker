import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from streamlit_calendar import calendar
import json

def render_calendar_view():
    st.header("Calendar View")

    # Prepare calendar events
    events = []
    for lesson in st.session_state.lessons.values():
        student = st.session_state.students.get(lesson.student_id)
        if not student:
            continue

        event = {
            'title': f"{student.name} - {lesson.topics[:30]}...",
            'start': datetime.combine(lesson.date, lesson.time).isoformat(),
            'end': (datetime.combine(lesson.date, lesson.time) + 
                   timedelta(minutes=lesson.duration)).isoformat(),
            'backgroundColor': {
                'Paid': '#28a745',
                'Pending': '#ffc107',
                'Overdue': '#dc3545'
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
        "height": 600
    }

    # Render calendar
    calendar(events=events, options=calendar_options)