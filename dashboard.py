import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_marks_chart(marks_data):
    if not marks_data:
        return None

    data = pd.DataFrame([
        {
            "Subject": item.subject,
            "Marks": item.marks
        }
        for item in marks_data
    ])

    fig, ax = plt.subplots()

    sns.barplot(
        data=data,
        x="Subject",
        y="Marks",
        ax=ax
    )

    ax.set_title("Student Marks")
    ax.set_ylim(0, 100)

    return fig


def create_attendance_chart(attendance_data):
    if not attendance_data:
        return None

    data = pd.DataFrame([
        {
            "Subject": item.subject,
            "Attendance": (
                item.attended_classes /
                item.total_classes * 100
                if item.total_classes > 0
                else 0
            )
        }
        for item in attendance_data
    ])

    fig, ax = plt.subplots()

    sns.barplot(
        data=data,
        x="Subject",
        y="Attendance",
        ax=ax
    )

    ax.set_title("Attendance Percentage")
    ax.set_ylim(0, 100)

    return fig