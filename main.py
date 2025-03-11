import streamlit as st
from utils import initialize_session_state
from components.student_management import render_student_management
from components.lesson_tracking import render_lesson_tracking
from components.calendar_view import render_calendar_view

# Page configuration
st.set_page_config(
    page_title="Özel Ders Yönetim Sistemi",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Sidebar navigation
st.sidebar.title("Özel Ders Yönetim Sistemi")
page = st.sidebar.radio(
    "Menü",
    ["Öğrenciler", "Dersler", "Takvim"]
)

# Main content
if page == "Öğrenciler":
    render_student_management()
elif page == "Dersler":
    render_lesson_tracking()
else:  # Calendar
    render_calendar_view()