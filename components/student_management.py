import streamlit as st
from models import Student, StudentGrade
from utils import add_student, get_student_lessons, delete_student

def render_student_management():
    st.header("Öğrenci Yönetimi")

    # Add new student form
    with st.expander("Yeni Öğrenci Ekle"):
        with st.form("new_student_form"):
            name = st.text_input("İsim")
            phone = st.text_input("Telefon")
            grade = st.selectbox(
                "Sınıf",
                options=[grade for grade in StudentGrade],
                format_func=lambda x: x.value
            )
            notes = st.text_area("Notlar")

            submitted = st.form_submit_button("Öğrenci Ekle")
            if submitted and name and phone:
                with st.spinner("Öğrenci ekleniyor..."):
                    add_student(name, phone, grade, notes)
                st.success("Öğrenci başarıyla eklendi!")
                st.rerun()

    # List all students
    st.subheader("Öğrenci Listesi")
    if not st.session_state.students:
        st.info("Henüz öğrenci eklenmemiş.")
        return

    for student in st.session_state.students.values():
        with st.expander(f"📚 {student.name}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Telefon:**", student.phone)
                st.write("**Sınıf:**", student.grade.value)
            with col2:
                lessons = get_student_lessons(student.id)
                st.write("**Toplam Ders:**", len(lessons))
                st.write("**Notlar:**", student.notes)

            # Delete student button
            if st.button("Öğrenciyi Sil", key=f"del_{student.id}"):
                delete_student(student.id)
                st.success("Öğrenci başarıyla silindi!")
                st.experimental_rerun()  # Force a complete page rerun