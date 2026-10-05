from database import Marks


def add_marks(session, roll_number, subject, marks):
    existing = (
        session.query(Marks)
        .filter_by(
            roll_number=roll_number,
            subject=subject
        )
        .first()
    )

    if existing:
        existing.marks = marks
    else:
        mark = Marks(
            roll_number=roll_number,
            subject=subject,
            marks=marks
        )

        session.add(mark)

    session.commit()

    return True, "Marks saved successfully."


def get_marks(session, roll_number=None):
    query = session.query(Marks)

    if roll_number:
        query = query.filter_by(roll_number=roll_number)

    return query.all()


def calculate_average(marks_list):
    if not marks_list:
        return 0

    values = [item.marks for item in marks_list]

    return sum(values) / len(values)