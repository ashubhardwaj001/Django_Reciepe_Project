from faker import Faker

fake = Faker()
from .models import *
import random

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






