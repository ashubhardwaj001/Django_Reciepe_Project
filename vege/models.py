from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

User = get_user_model()


class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Receipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True, blank=True)
    receipe_name = models.CharField(max_length=100)
    receipe_description = models.TextField()
    receipe_image = models.ImageField(upload_to='recipe')
    receipe_view_count = models.IntegerField(default=1)
    

    


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department
    
    class Meta:
        ordering = ['department']


class StudentID(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.student_id
    

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subject_name    

class Student(models.Model):
    student_id = models.ForeignKey(StudentID, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=10)
    student_address = models.TextField()
    is_deleted = models.BooleanField(default=False)

    objects = StudentManager()
    admin_objects = models.Manager()  # This will include all objects, including deleted ones

    def __str__(self) -> str:
        return self.student_name
    
    class Meta:
        ordering = ['student_name']
        verbose_name = 'Student'

class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, related_name= "studentmarks", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.student.student_name} - {self.subject.subject_name} - {self.marks}"
    
    class Meta:
        unique_together = ('student', 'subject' )


class ReportCard(models.Model):
    student = models.ForeignKey(Student, related_name="studentreportcard", on_delete=models.CASCADE)
    student_rank = models.IntegerField(default=0)
    date_of_report_card_generation = models.DateField(auto_now_add=True)


    class Meta:
        unique_together = ('student_rank', 'date_of_report_card_generation')
