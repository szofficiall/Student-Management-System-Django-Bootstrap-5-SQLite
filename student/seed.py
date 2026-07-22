from faker import Faker
from .models import *
import random
from django.db.models import Sum

fake = Faker()


def seed_deparment():
    departments = [
        "Artificial Intelligence",
        "Computer Science",
        "Software Engineering",
        "Mass Communication",
        "Physics",
        "Biology",
        "Mathemathics",
    ]

    for dept in departments:
        Department.objects.get_or_create(department=dept)

    print("Departments created successfully.")


def feed_subjects():
    subjects = ["Python", "DSA", "OOP", "PF", "DLD", "OS", "PDC", "TOA"]

    for subject in subjects:
        Subject.objects.get_or_create(subject_name=subject)

    print("Created Succesfully")


def feed_db(n=10):
    departments = list(Department.objects.all())

    if not departments:
        print("Create Deparment First")
        return

    for _ in range(n):
        student_id = f"STU - {random.randint(1000,9999)}"
        student_id_obj = StudentId.objects.create(student_id=student_id)

        Student.objects.create(
            student=student_id_obj,
            department=random.choice(departments),
            student_name=fake.name(),
            student_email=fake.unique.email(),
            student_age=random.randint(18, 30),
            student_address=fake.address(),
        )

    print(f"{n} Students created successfully.")


# -----------------------------
# Create Subject Marks
# -----------------------------
def student_subject_marks():
    students = Student.objects.all()
    subjects = Subject.objects.all()

    if not students.exists():
        print("No students found.")
        return

    if not subjects.exists():
        print("No subjects found.")
        return

    created = 0

    for student in students:
        for subject in subjects:
            _, is_created = SubjectMarks.objects.get_or_create(
                student=student,
                subject=subject,
                defaults={"marks": random.randint(0, 100)},
            )

            if is_created:
                created += 1

    print(f"{created} Subject Marks created successfully.")
