from django.db import models

# Create your models here.
class Student(models.Model):
    student_id= models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    surname= models.CharField(max_length=100)
    program= models.CharField(max_length=100)
    course= models.CharField(max_length=100)
    marks= models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name + ' ' + self.surname

#class program

# class course

# class mark

# class teacher




