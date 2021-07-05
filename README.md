 ## Location-based Class Attendance System
 **Application to replace the attendance records on PAPER with digital records**
 ![Class Attendance System](/images/index.png)
 
In this web-application, we used following technologies:
 + Django framework
 + JavaScript
 + Chartjs
 + Bootstrap
 + SQLite
 

**Features**

+ Admin-panel for teachers
  - Admins can CRUD subjects,class,classroom location,student records.
  
+ Students can view attendance percentage, timetable.
  - Students can late up to 10 minutes(Teachers can change this variable), otherwise attendance-take function will not available.
  - Students must be within classroom area(about 10 metres), otherwise the attendance-take function will not available.
  - Students can have only ONE success add_attendance.(This means if he/she already enrolled, then he/she can't add new attendance even if he/she meets above 2 conditions.)
  - To take attendance successfully, students must meet above conditions.


## Installation

`git clone https://github.com/ThwinHtetWin/attendance_system.git`

**Install requirements**

`pip3 install -r requirements.txt `

**Steps to add new records to database**
1. add new classroom
2. add new subject
3. add new classroom-subject
4. add new timetable

sample_db.sqlite3 is a sample database before students get in-touch.

## How To Run Application

`python3 manage.py runserver`
