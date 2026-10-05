import streamlit as st
import pandas as pd

from database import get_session
from student import (
    add_student,
    get_all_students,
    search_students,
    delete_student
)
from attendance import (
    add_attendance,
    get_attendance,
    calculate_percentage
)
from marks import (
    add_marks,
    get_marks,
    calculate_average
)
from ai_analysis import (
    predict_performance,
    get_performance_status,
    get_recommendation
)
from dashboard import (
    create_marks_chart,
    create_attendance_chart
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Student Management System",
    page_icon="🎓",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎓 AI-Based Student Management System")

st.write(
    "Manage student information, attendance, marks "
    "and analyze student performance using Machine Learning."
)


# --------------------------------------------------
# DATABASE SESSION
# --------------------------------------------------

session = get_session()


# --------------------------------------------------
# SIDEBAR MENU
# --------------------------------------------------

st.sidebar.title("📚 Navigation")

menu = st.sidebar.radio(
    "Select a module",
    [
        "🏠 Home",
        "👨‍🎓 Student Management",
        "📋 Attendance",
        "📝 Marks",
        "🤖 AI Performance Analysis",
        "📊 Dashboard"
    ]
)


# ==================================================
# HOME
# ==================================================

if menu == "🏠 Home":

    st.header("Welcome! 👋")

    st.write(
        """
        This application helps manage student academic information
        in one place.
        """
    )

    students = get_all_students(session)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "👨‍🎓 Total Students",
            len(students)
        )

    with col2:
        st.metric(
            "📋 Attendance Module",
            "Active"
        )

    with col3:
        st.metric(
            "🤖 AI Analysis",
            "Active"
        )

    st.info(
        "Use the menu on the left to manage students, "
        "attendance, marks and performance."
    )


# ==================================================
# STUDENT MANAGEMENT
# ==================================================

elif menu == "👨‍🎓 Student Management":

    st.header("👨‍🎓 Student Management")

    tab1, tab2, tab3 = st.tabs(
        [
            "➕ Add Student",
            "🔍 Search Students",
            "🗑️ Delete Student"
        ]
    )

    # ----------------------------------------------
    # ADD STUDENT
    # ----------------------------------------------

    with tab1:

        st.subheader("Add New Student")

        with st.form("student_form"):

            col1, col2 = st.columns(2)

            with col1:

                roll_number = st.text_input(
                    "Roll Number"
                )

                name = st.text_input(
                    "Student Name"
                )

                branch = st.text_input(
                    "Branch",
                    value="Data Science"
                )

                year = st.number_input(
                    "Year",
                    min_value=1,
                    max_value=4,
                    value=2
                )

            with col2:

                section = st.text_input(
                    "Section",
                    value="DS-D"
                )

                email = st.text_input(
                    "Email"
                )

                phone = st.text_input(
                    "Phone Number"
                )

            submit = st.form_submit_button(
                "Add Student"
            )

        if submit:

            if not roll_number or not name:

                st.error(
                    "Roll number and student name are required."
                )

            else:

                success, message = add_student(
                    session,
                    roll_number,
                    name,
                    branch,
                    year,
                    section,
                    email,
                    phone
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)


    # ----------------------------------------------
    # SEARCH STUDENTS
    # ----------------------------------------------

    with tab2:

        st.subheader("🔍 Search Students")

        keyword = st.text_input(
            "Enter roll number or student name"
        )

        if keyword:

            students = search_students(
                session,
                keyword
            )

        else:

            students = get_all_students(
                session
            )

        if students:

            data = []

            for student in students:

                data.append({
                    "ID": student.id,
                    "Roll Number": student.roll_number,
                    "Name": student.name,
                    "Branch": student.branch,
                    "Year": student.year,
                    "Section": student.section,
                    "Email": student.email,
                    "Phone": student.phone
                })

            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True
            )

        else:

            st.info("No students found.")


    # ----------------------------------------------
    # DELETE STUDENT
    # ----------------------------------------------

    with tab3:

        st.subheader("🗑️ Delete Student")

        students = get_all_students(session)

        if students:

            student_options = {
                f"{s.roll_number} - {s.name}": s.id
                for s in students
            }

            selected = st.selectbox(
                "Select student",
                list(student_options.keys())
            )

            if st.button("Delete Student"):

                student_id = student_options[
                    selected
                ]

                success, message = delete_student(
                    session,
                    student_id
                )

                if success:
                    st.success(message)
                else:
                    st.error(message)

        else:

            st.info("No students available.")


# ==================================================
# ATTENDANCE
# ==================================================

elif menu == "📋 Attendance":

    st.header("📋 Attendance Management")

    students = get_all_students(session)

    if not students:

        st.warning(
            "Please add a student first."
        )

    else:

        roll_numbers = [
            student.roll_number
            for student in students
        ]

        selected_roll = st.selectbox(
            "Select Student",
            roll_numbers
        )

        subject = st.text_input(
            "Subject"
        )

        col1, col2 = st.columns(2)

        with col1:

            total_classes = st.number_input(
                "Total Classes",
                min_value=0,
                value=0
            )

        with col2:

            attended_classes = st.number_input(
                "Attended Classes",
                min_value=0,
                value=0
            )

        if st.button("Save Attendance"):

            if not subject:

                st.error(
                    "Please enter a subject."
                )

            elif attended_classes > total_classes:

                st.error(
                    "Attended classes cannot be greater "
                    "than total classes."
                )

            else:

                success, message = add_attendance(
                    session,
                    selected_roll,
                    subject,
                    total_classes,
                    attended_classes
                )

                if success:

                    percentage = calculate_percentage(
                        total_classes,
                        attended_classes
                    )

                    st.success(message)

                    st.metric(
                        "Attendance Percentage",
                        f"{percentage:.2f}%"
                    )


        st.divider()

        st.subheader("Attendance Records")

        records = get_attendance(
            session,
            selected_roll
        )

        if records:

            data = []

            for record in records:

                percentage = calculate_percentage(
                    record.total_classes,
                    record.attended_classes
                )

                data.append({
                    "Subject": record.subject,
                    "Total Classes": record.total_classes,
                    "Attended": record.attended_classes,
                    "Attendance %": round(
                        percentage,
                        2
                    )
                })

            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True
            )

        else:

            st.info(
                "No attendance records found."
            )


# ==================================================
# MARKS
# ==================================================

elif menu == "📝 Marks":

    st.header("📝 Marks Management")

    students = get_all_students(session)

    if not students:

        st.warning(
            "Please add a student first."
        )

    else:

        roll_numbers = [
            student.roll_number
            for student in students
        ]

        selected_roll = st.selectbox(
            "Select Student",
            roll_numbers
        )

        subject = st.text_input(
            "Subject"
        )

        marks_value = st.number_input(
            "Marks",
            min_value=0.0,
            max_value=100.0,
            value=0.0
        )

        if st.button("Save Marks"):

            if not subject:

                st.error(
                    "Please enter a subject."
                )

            else:

                success, message = add_marks(
                    session,
                    selected_roll,
                    subject,
                    marks_value
                )

                st.success(message)


        st.divider()

        st.subheader("Marks Records")

        records = get_marks(
            session,
            selected_roll
        )

        if records:

            data = []

            for record in records:

                data.append({
                    "Subject": record.subject,
                    "Marks": record.marks
                })

            st.dataframe(
                pd.DataFrame(data),
                use_container_width=True
            )

            average = calculate_average(
                records
            )

            st.metric(
                "Average Marks",
                f"{average:.2f}"
            )

        else:

            st.info(
                "No marks records found."
            )


# ==================================================
# AI PERFORMANCE ANALYSIS
# ==================================================

elif menu == "🤖 AI Performance Analysis":

    st.header("🤖 AI-Based Student Performance Analysis")

    students = get_all_students(session)

    if not students:

        st.warning(
            "Please add students first."
        )

    else:

        roll_numbers = [
            student.roll_number
            for student in students
        ]

        selected_roll = st.selectbox(
            "Select Student",
            roll_numbers
        )

        attendance_records = get_attendance(
            session,
            selected_roll
        )

        marks_records = get_marks(
            session,
            selected_roll
        )

        if not attendance_records:

            st.warning(
                "Please enter attendance data first."
            )

        elif not marks_records:

            st.warning(
                "Please enter marks first."
            )

        else:

            total_classes = sum(
                item.total_classes
                for item in attendance_records
            )

            attended_classes = sum(
                item.attended_classes
                for item in attendance_records
            )

            attendance_percentage = calculate_percentage(
                total_classes,
                attended_classes
            )

            average_marks = calculate_average(
                marks_records
            )

            prediction = predict_performance(
                attendance_percentage,
                average_marks
            )

            status = get_performance_status(
                prediction
            )

            recommendations = get_recommendation(
                attendance_percentage,
                average_marks
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Attendance",
                    f"{attendance_percentage:.2f}%"
                )

            with col2:

                st.metric(
                    "Average Marks",
                    f"{average_marks:.2f}"
                )

            with col3:

                st.metric(
                    "Predicted Performance",
                    f"{prediction:.2f}%"
                )

            st.subheader(
                f"Performance Status: {status}"
            )

            for recommendation in recommendations:

                st.info(
                    f"💡 {recommendation}"
                )


# ==================================================
# DASHBOARD
# ==================================================

elif menu == "📊 Dashboard":

    st.header("📊 Student Dashboard")

    students = get_all_students(session)

    st.metric(
        "Total Students",
        len(students)
    )

    if students:

        selected_roll = st.selectbox(
            "Select Student",
            [
                student.roll_number
                for student in students
            ]
        )

        marks_records = get_marks(
            session,
            selected_roll
        )

        attendance_records = get_attendance(
            session,
            selected_roll
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("📝 Marks")

            marks_chart = create_marks_chart(
                marks_records
            )

            if marks_chart:

                st.pyplot(
                    marks_chart
                )

            else:

                st.info(
                    "No marks available."
                )

        with col2:

            st.subheader("📋 Attendance")

            attendance_chart = create_attendance_chart(
                attendance_records
            )

            if attendance_chart:

                st.pyplot(
                    attendance_chart
                )

            else:

                st.info(
                    "No attendance available."
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.sidebar.divider()

st.sidebar.caption(
    "AI-Based Student Management System"
)

st.sidebar.caption(
    "Python 3.11.9 | Streamlit | SQLAlchemy | Scikit-learn"
)