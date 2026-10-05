from database import Student


def add_student(
    session,
    roll_number,
    name,
    branch,
    year,
    section,
    email,
    phone
):
    existing_student = (
        session.query(Student)
        .filter_by(roll_number=roll_number)
        .first()
    )

    if existing_student:
        return False, "Student with this roll number already exists."

    student = Student(
        roll_number=roll_number,
        name=name,
        branch=branch,
        year=year,
        section=section,
        email=email,
        phone=phone
    )

    session.add(student)
    session.commit()

    return True, "Student added successfully."


def get_all_students(session):
    return session.query(Student).order_by(Student.id.desc()).all()


def search_students(session, keyword):
    return (
        session.query(Student)
        .filter(
            (Student.roll_number.ilike(f"%{keyword}%"))
            | (Student.name.ilike(f"%{keyword}%"))
        )
        .all()
    )


def delete_student(session, student_id):
    student = session.query(Student).filter_by(id=student_id).first()

    if not student:
        return False, "Student not found."

    session.delete(student)
    session.commit()

    return True, "Student deleted successfully."