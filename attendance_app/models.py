from django.db import models,IntegrityError
from django.contrib.auth.models import AbstractUser
import datetime
# Create your models here.

PERIODS = [
    ('08:00am-08:50am','08:00am-08:50am'),
    ('09:00am-09:50am','09:00am-09:50am'),
    ('08:00am-09:50am','08:00am-09:50am'),
    ('09:00am-10:50am','09:00am-10:50am'),
    ('10:00am-11:50am','10:00am-11:50am'),
    ('10:00am-10:50am','10:00am-10:50am'),
    ('11:00am-11:50am','11:00am-11:50am'),
    ('01:00pm-01:50pm','01:00pm-01:50pm'),
    ('02:00pm-02:50pm','02:00pm-02:50pm'),
    ('01:00pm-02:50pm','01:00pm-02:50pm'),
    ('03:00pm-03:50pm','03:00pm-03:50pm'),
    ('02:00pm:03:50pm','02:00pm:03:50pm')
]

DAYS = [
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday')
]

class User(AbstractUser):
    attending_year = models.CharField(max_length=10)
    roll_no_prefix = models.CharField(max_length=10,default='')
    roll_no_number = models.IntegerField(default=0)
    roll_number = models.CharField(max_length=20,default='')

    classroom      = models.CharField(max_length=20,blank=True)

    def save(self,*args,**kwargs):
        self.roll_number = self.roll_no_prefix + str(self.roll_no_number)
        super(User,self).save(*args,**kwargs)

    def __str__(self):
        return f'{self.username}({self.roll_number})'

class Classroom(models.Model):
    id = models.CharField(primary_key=True,max_length=20) #classromid
    class_name = models.CharField(max_length=20)
    semester = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=18,decimal_places=15,default=10.00)
    longitude = models.DecimalField(max_digits=18,decimal_places=15,default=10.00)

    def __str__(self):
        return f'{self.class_name}({self.id})'

class FirstYearStudent(models.Model):
    name = models.CharField(max_length=30)
    roll_number = models.CharField(max_length=10,primary_key=True)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}({self.roll_number})'

class SecondYearStudent(models.Model):
    name = models.CharField(max_length=30)
    roll_number = models.CharField(max_length=10,primary_key=True)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}({self.roll_number})'

class ThirdYearStudent(models.Model):
    name = models.CharField(max_length=30)
    roll_number = models.CharField(max_length=10,primary_key=True)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}({self.roll_number})'

class FourthYearStudent(models.Model):
    name = models.CharField(max_length=30)
    roll_number = models.CharField(max_length=10,primary_key=True)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}({self.roll_number})'

class Subject(models.Model):
    
    module_no = models.CharField(max_length=10,primary_key=True)
    module_name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.module_name}({self.module_no})'

class ClassroomSubject(models.Model):
    class_id = models.ForeignKey(Classroom,on_delete=models.CASCADE) 
    subject  = models.ForeignKey(Subject,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('class_id', 'subject'),)

    def __str__(self):
        classroom = Classroom.objects.get(id=self.class_id_id)
        subject = Subject.objects.get(module_no=self.subject_id)
        return f'{classroom}-{subject}'

class Timetable(models.Model):

    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE,default='') 
    subject = models.ForeignKey(ClassroomSubject,on_delete=models.CASCADE)
    #period = models.CharField(max_length=50, choices=PERIODS, default='00:00 - 00:00')
    day = models.CharField(max_length=15, choices=DAYS)
    start_time = models.CharField(max_length=20,default='')
    end_time = models.CharField(max_length=20,default='')

    def __str__(self):
        return f'{self.subject}/{self.day}/{self.start_time}:{self.end_time}'

class Attendance(models.Model):

    student   = models.ForeignKey(User,on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom,on_delete=models.CASCADE)
    subject   = models.ForeignKey(Timetable,on_delete=models.CASCADE)
    time      = models.TimeField(default='0:00:00')
    date      = models.DateField()

    def __str__(self):
        
        return f'{self.student.username}-{self.subject.subject.subject_id}'