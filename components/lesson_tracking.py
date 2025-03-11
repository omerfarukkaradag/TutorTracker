import streamlit as st
from datetime import datetime, time
from models import PaymentStatus
from utils import add_lesson, get_student_lessons

def render_lesson_tracking():
    st.header("Ders Takibi")

    # Add new lesson form
    with st.expander("Yeni Ders Ekle"):
        with st.form("new_lesson_form"):
            if not st.session_state.students:
                st.warning("Lütfen önce öğrenci ekleyiniz.")
                st.form_submit_button("Ders Ekle", disabled=True)
                return

            student_id = st.selectbox(
                "Öğrenci",
                options=list(st.session_state.students.keys()),
                format_func=lambda x: st.session_state.students[x].name
            )

            col1, col2 = st.columns(2)
            with col1:
                date = st.date_input("Tarih")
            with col2:
                time_input = st.time_input("Saat")

            duration = st.number_input("Süre (dakika)", min_value=15, value=60, step=15)
            topics = st.text_area("İşlenen Konular")
            payment_status = st.selectbox(
                "Ödeme Durumu",
                options=[status for status in PaymentStatus],
                format_func=lambda x: x.value
            )
            notes = st.text_area("Notlar")

            submitted = st.form_submit_button("Ders Ekle")
            if submitted and student_id and topics:
                with st.spinner("Ders ekleniyor..."):
                    add_lesson(
                        student_id=student_id,
                        date=date,
                        time=time_input,
                        duration=duration,
                        topics=topics,
                        payment_status=payment_status,
                        notes=notes
                    )
                st.success("Ders başarıyla eklendi!")
                st.rerun()

    # List lessons by student
    st.subheader("Ders Geçmişi")
    if not st.session_state.students:
        st.info("Henüz öğrenci eklenmemiş.")
        return

    selected_student = st.selectbox(
        "Öğrenci Seç",
        options=list(st.session_state.students.keys()),
        format_func=lambda x: st.session_state.students[x].name,
        key="lesson_history_student"
    )

    lessons = get_student_lessons(selected_student)
    if not lessons:
        st.info("Bu öğrenci için ders kaydı bulunmamaktadır.")
        return

    for lesson in sorted(lessons, key=lambda x: x.date, reverse=True):
        with st.expander(f"📖 {lesson.date.strftime('%d.%m.%Y')} - {lesson.time.strftime('%H:%M')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Süre:**", f"{lesson.duration} dakika")
                st.write("**Konular:**", lesson.topics)
            with col2:
                # Add payment status editing
                new_status = st.selectbox(
                    "Ödeme Durumu",
                    options=[status for status in PaymentStatus],
                    index=list(PaymentStatus).index(lesson.payment_status),
                    key=f"payment_status_{lesson.id}",
                    format_func=lambda x: x.value
                )
                if new_status != lesson.payment_status:
                    st.session_state.lessons[lesson.id].payment_status = new_status
                    st.success("Ödeme durumu güncellendi!")
                    st.rerun()

                st.write("**Notlar:**", lesson.notes)

            # Delete lesson button
            if st.button("Dersi Sil", key=f"del_lesson_{lesson.id}"):
                del st.session_state.lessons[lesson.id]
                st.success("Ders başarıyla silindi!")
                st.rerun()