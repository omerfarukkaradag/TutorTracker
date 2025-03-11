import streamlit as st
from datetime import datetime, time
from models import PaymentStatus
from utils import add_lesson, get_student_lessons

def render_lesson_tracking():
    st.header("Lesson Tracking")

    # Add new lesson form
    with st.expander("Add New Lesson"):
        with st.form("new_lesson_form"):
            if not st.session_state.students:
                st.warning("Please add students first.")
                st.form_submit_button("Add Lesson", disabled=True)
                return

            student_id = st.selectbox(
                "Student",
                options=list(st.session_state.students.keys()),
                format_func=lambda x: st.session_state.students[x].name
            )

            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Date")
            with col2:
                time_input = st.time_input("Time")

            duration = st.number_input("Duration (minutes)", min_value=15, value=60, step=15)
            topics = st.text_area("Topics Covered")
            payment_status = st.selectbox(
                "Payment Status",
                options=[status.value for status in PaymentStatus]
            )
            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Add Lesson")
            if submitted and student_id and topics:
                with st.spinner("Adding lesson..."):
                    add_lesson(
                        student_id=student_id,
                        date=datetime.combine(date, time_input),
                        time=time_input,
                        duration=duration,
                        topics=topics,
                        payment_status=PaymentStatus(payment_status),
                        notes=notes
                    )
                st.success("Lesson added successfully!")
                st.rerun()

    # List lessons by student
    st.subheader("Lesson History")
    if not st.session_state.students:
        st.info("No students added yet.")
        return

    selected_student = st.selectbox(
        "Select Student",
        options=list(st.session_state.students.keys()),
        format_func=lambda x: st.session_state.students[x].name,
        key="lesson_history_student"
    )

    lessons = get_student_lessons(selected_student)
    if not lessons:
        st.info("No lessons recorded for this student.")
        return

    for lesson in sorted(lessons, key=lambda x: x.date, reverse=True):
        with st.expander(f"📖 {lesson.date.strftime('%Y-%m-%d')} - {lesson.time.strftime('%I:%M %p')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Duration:**", f"{lesson.duration} minutes")
                st.write("**Topics:**", lesson.topics)
            with col2:
                st.write("**Payment Status:**", lesson.payment_status.value)
                st.write("**Notes:**", lesson.notes)

            # Delete lesson button
            if st.button("Delete Lesson", key=f"del_lesson_{lesson.id}"):
                del st.session_state.lessons[lesson.id]
                st.success("Lesson deleted successfully!")
                st.rerun()