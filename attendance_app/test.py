timetable = {'Monday': {'ENG-2001': ('9:00am', '9:50am'), 'CS-2103': ('10:00am', '11:50am'), 'CS-2104': ('1:00pm', '2:50pm')}, 'Tuesday': {'ENG-2001': ('9:00am', '9:50am'), 'CS-2102': ('10:00am', '11:50am'), 'CS-2101': ('1:00pm', '1:50pm'), 'CS-2104': ('2:00pm', '3:50pm')}, 'Wednesday': {'CS-2103': ('9:00am', '10:50am'), 'CS-2102': ('11:00am', '11:50am'), 'CS-2101': ('1:00pm', '2:50pm')}, 'Thursday': {'ENG-2001': ('8:00am', '9:50am'), 'CS-2105': ('10:00am', '11:50am'), 'CS-2101': ('1:00pm', '2:50pm')}, 'Friday': {'CS-2103': ('9:00am', '9:50am'), 'CS-2105': ('10:00am', '11:50am'), 'CS-2102': ('1:00pm', '2:50pm')}}
days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

for day in days:
    for i in timetable[day]:
        print(timetable[day][i][0])