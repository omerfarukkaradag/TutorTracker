import streamlit as st
from utils import initialize_session_state
from components.student_management import render_student_management
from components.lesson_tracking import render_lesson_tracking
from components.calendar_view import render_calendar_view

# Page configuration
st.set_page_config(
    page_title="Tutor Management System",
    page_icon="📚",
    layout="wide"
)

# Initialize session state
initialize_session_state()

# Sidebar navigation
st.sidebar.title("Tutor Management System")
page = st.sidebar.radio(
    "Navigation",
    ["Students", "Lessons", "Calendar"]
)

# Main content
if page == "Students":
    render_student_management()
elif page == "Lessons":
    render_lesson_tracking()
else:  # Calendar
    render_calendar_view()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ by Your Tutor Assistant")
