from attendance_system.models import *

default_periods = ['08:00am-08:50am','09:00am-09:50am','10:00am-10:50am','11:00am-11:50am','01:00am-01:50am','02:00am-02:50am','03:00am-03:50am']
monday_timetable = Timetable.objects.filter(classroom_id="CS01",day="Monday")

for item in monday_timetable:
    print(item)