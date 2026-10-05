from database import Attendance


def add_attendance(
    session,
    roll_number,
    subject,
    total_classes,
    attended_classes
):
    existing = (
        session.query(Attendance)
        .filter_by(
            roll_number=roll_number,
            subject=subject
        )
        .first()
    )

    if existing:
        existing.total_classes = total_classes
        existing.attended_classes = attended_classes
    else:
        attendance = Attendance(
            roll_number=roll_number,
            subject=subject,
            total_classes=total_classes,
            attended_classes=attended_classes
        )

        session.add(attendance)

    session.commit()

    return True, "Attendance saved successfully."


def get_attendance(session, roll_number=None):
    query = session.query(Attendance)

    if roll_number:
        query = query.filter_by(roll_number=roll_number)

    return query.all()


def calculate_percentage(total_classes, attended_classes):
    if total_classes == 0:
        return 0

    return (attended_classes / total_classes) * 100