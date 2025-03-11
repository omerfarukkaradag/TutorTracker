import streamlit as st
from models import Student
from utils import add_student, get_student_lessons

def render_student_management():
    st.header("Student Management")

    # Add new student form
    with st.expander("Add New Student"):
        with st.form("new_student_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            notes = st.text_area("Notes")

            submitted = st.form_submit_button("Add Student")
            if submitted and name and email and phone:
                with st.spinner("Adding student..."):
                    add_student(name, email, phone, notes)
                st.success("Student added successfully!")
                st.rerun()

    # List all students
    st.subheader("Student List")
    if not st.session_state.students:
        st.info("No students added yet.")
        return

    for student in st.session_state.students.values():
        with st.expander(f"📚 {student.name}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Email:**", student.email)
                st.write("**Phone:**", student.phone)
            with col2:
                lessons = get_student_lessons(student.id)
                st.write("**Total Lessons:**", len(lessons))
                st.write("**Notes:**", student.notes)

            # Delete student button
            if st.button("Delete Student", key=f"del_{student.id}"):
                del st.session_state.students[student.id]
                st.success("Student deleted successfully!")
                st.rerun()