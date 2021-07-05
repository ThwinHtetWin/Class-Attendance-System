from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(FirstYearStudent)
admin.site.register(SecondYearStudent)
admin.site.register(ThirdYearStudent)
admin.site.register(FourthYearStudent)
admin.site.register(Classroom)
admin.site.register(Subject)
admin.site.register(ClassroomSubject)
admin.site.register(Timetable)
#admin.site.register(AttendanceClassroom)
admin.site.register(Attendance)