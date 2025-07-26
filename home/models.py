from django.db import models

# Create your models here.

class Student(models.Model):
    #id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=255)
    image = models.ImageField()
    file = models.FileField()


class Car(models.Model):

    car_name = models.CharField(max_length=100)
    speed = models.IntegerField()

    def __str__(self):
        return self.car_name