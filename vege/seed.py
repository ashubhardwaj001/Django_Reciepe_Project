from faker import Faker

fake = Faker()
from .models import *
import random
from django.db.models import Sum


def create_subject_marks(n):

    student_objs = Student.objects.all()
    for student in student_objs:

        subjects = Subject.objects.all()
        for subject in subjects:
            marks = random.randint(0, 100)
            SubjectMarks.objects.create(
                student=student,
                subject=subject,
                marks=marks
            )

def seed_db(n=10) -> None:

    try:
    
        for _ in range(n):

            department_objs = Department.objects.all()
            random_index = random.randint(0, len(department_objs) - 1)
            department = department_objs[random_index]
            student_id = f'STU-0{random.randint(100, 999)}'
            student_name = fake.name()
            student_email = fake.email()
            student_age = random.randint(18, 25)
            student_address = fake.address()


            student_id_obj = StudentID.objects.create(student_id = student_id)

            student_obj = Student.objects.create(
                        student_id=student_id_obj,
                        department=department,
                        student_name=student_name,
                        student_email=student_email,
                        student_age=student_age,
                        student_address=student_address
                        )
            
    
    except Exception as e:
        print(e)


def generate_report_card():

    current_rank = -1
    
    ranks = Student.objects.annotate(marks = Sum('studentmarks__marks')).order_by('-marks','-student_age')

    i = 1

    for rank in ranks:
        ReportCard.objects.create(
            student=rank,
            student_rank=i
        )
        i += 1






