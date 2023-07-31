from django.db import models

# Create your models here.
class College(models.Model):
    college_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Streams(models.Model):
    branch_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    reg_no = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    branch = models.ForeignKey('Streams', on_delete=models.CASCADE)
    college = models.ForeignKey('College', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} "
    

class CollegeStream(models.Model):
    college = models.ForeignKey('College', on_delete=models.CASCADE)
    branch = models.ForeignKey('Streams', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.college.name}"
    
