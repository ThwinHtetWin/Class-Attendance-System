from django.shortcuts import render
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required  
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView
from .models import *
from datetime import datetime,date,timedelta
from dateutil.parser import parse
from haversine import haversine, Unit
from .forms import StudentRegisterForm
import time,json

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "attendance_system/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "attendance_system/login.html")

def logout_view(request):

    logout(request)
    return HttpResponseRedirect(reverse("index"))

def StudentRegisterView(request):
    form = StudentRegisterForm()

    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("enrollment"))
        else:
            form = StudentRegisterForm()


    return render(request, 'attendance_system/register.html', {'form': form})

@login_required
def enrollment(request):
    
    id = request.user.id
    print(id) #5

    name           = request.user.username
    roll_no_prefix = request.user.roll_no_prefix
    roll_number    = request.user.roll_number
    attending_year = request.user.attending_year
    classroom      = request.user.classroom
    print(id,name,roll_no_prefix,roll_number,attending_year,classroom)

    if attending_year == 'FirstYear' and roll_no_prefix == '1KaTha/':
        subjects = ClassroomSubject.objects.filter(class_id="CS-ROOM-01")

    elif attending_year == 'SecondYear' and roll_no_prefix == '2KaTha/':
        subjects = ClassroomSubject.objects.filter(class_id="CS-ROOM-02")

    elif attending_year == 'ThirdYear' and roll_no_prefix == '3KaTha/':
        subjects = ClassroomSubject.objects.filter(class_id="CS-ROOM-03")

    elif attending_year == 'FourthYear' and roll_no_prefix == '4KaTha/':
        subjects = ClassroomSubject.objects.filter(class_id="CS-ROOM-04")
    
    if request.method == "POST":
        
        try:
            if attending_year == 'FirstYear' and roll_no_prefix == '1KaTha/':
                FirstYearStudent.objects.create(name=request.user.username,roll_number=roll_number,classroom_id="CS-ROOM-01")
                a = User.objects.get(id=id)
                a.classroom = 'CS-ROOM-01'
                a.save()

                return HttpResponseRedirect(reverse("index"))
            
            elif attending_year == 'SecondYear' and roll_no_prefix == '2KaTha/':
                SecondYearStudent.objects.create(name=request.user.username,roll_number=roll_number,classroom_id="CS-ROOM-02")
                a = User.objects.get(id=id)
                a.classroom = 'CS-ROOM-02'
                a.save()

                return HttpResponseRedirect(reverse("index"))

            elif attending_year == 'ThirdYear' and roll_no_prefix == '3KaTha/':
                ThirdYearStudent.objects.create(name=request.user.username,roll_number=roll_number,classroom_id="CS-ROOM-03")
                a = User.objects.get(id=id)
                a.classroom = 'CS-ROOM-03'
                a.save()

                return HttpResponseRedirect(reverse("index"))

            elif attending_year == 'FourthYear' and roll_no_prefix == '4KaTha/':
                FourthYearStudent.objects.create(name=request.user.username,roll_number=roll_number,classroom_id="CS-ROOM-04")
                a = User.objects.get(id=id)
                a.classroom = 'CS-ROOM-04'
                a.save()

                return HttpResponseRedirect(reverse("index"))

        except IntegrityError:
            return render(request,'attendance_system/error.html',{'msg':'You\'re already enrolled.'})
    
    elif request.method == "GET":
        
        return render(request,'attendance_system/enrollment.html',{
            'subjects':subjects,
            'name':name,
            'attending_year':attending_year,
            'roll_number':roll_number
        })
    
    else:

        return render(request,'attendance_system/error.html',{'msg':'Method not allowed.'})

def index(request):

    if request.user.is_authenticated:
        print("logged in.")
        
    else:
        print("Not logged in.")

    return render(request,'attendance_system/index.html')

def timetable(request):

    attending_year = request.user.attending_year
    classroom      = request.user.classroom
    day            = datetime.now().date().strftime("%A")

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday"]
    timetable = {}

    for day in days:
        s = Timetable.objects.filter(classroom_id=classroom,day=day)
        timetable[day] = {}
        for i in s:
            timetable[day][i.subject.subject.module_no] = {}
            timetable[day][i.subject.subject.module_no]["start_time"] = i.start_time
            timetable[day][i.subject.subject.module_no]["end_time"] = i.end_time
    
    return render(request,'attendance_system/timetable.html',{
        "timetable":timetable,
        "attending_year":attending_year,
        "days":days,
        "s":s
        })


@login_required
def attendance(request):

    id = request.user.id #5

    attending_year = request.user.attending_year
    classroom      = request.user.classroom
    day            = datetime.now().date().strftime("%A")
    today          = date.today()

    subjects = Timetable.objects.filter(classroom_id=classroom,day=day)

    attended_subjects   = Attendance.objects.filter(student_id=id,classroom_id=classroom,date=today)
    #attended_subjects   = Attendance.objects.filter(student_id=10,classroom_id="CS-ROOM-02",date="2021-06-30")
    attended_subject_id = [sub.subject_id for sub in attended_subjects] #[28, 29]
   
    #timetable = Timetable.objects.filter(day="Wednesday")
    return render(request,'attendance_system/attendance.html',{
        'subjects':subjects,
        'attended_subject_id':attended_subject_id,
        'day':day
        })

def late(sub_time_obj):

    current_time = datetime.now()
    #print("current_time : ",current_time)
    #print("sub_time_obj : ",sub_time_obj)

    diff = current_time - sub_time_obj
    late_for = int(diff.total_seconds()//60)
    #print(f'late_for    : {late_for} mins')

    if late_for <= 115:
        return True
    elif late_for < 0:
        return False
    else:
        return False

def is_in_class(student_latitude,student_longitude,classroom):
    class_lat = Classroom.objects.get(id=classroom).latitude
    class_long = Classroom.objects.get(id=classroom).longitude

    #print(f'is_in_class classid : {classroom}')

    class_loc = (class_lat,class_long)
    student_loc = (student_latitude,student_longitude)

    distance = haversine(class_loc,student_loc,Unit.FEET)
    #print(f"in class : {class_lat} , distance is {distance} ft")

    if distance <= 10:
        return True
    elif distance < 0:
        return False
    else:
        return False

@login_required
def add_attendance(request):
    
    if request.method == "POST":
        
        #print("i am json : ",request.body.decode('utf-8')) #{"latitude":21.9952,"longitude":97.9988,"subject_timetable_id":"9"}
        att_info = json.loads(request.body.decode('utf-8'))
        #print(f"subject_timetable_id : {att_info['subject_timetable_id']}")
        
        subject_timetable_id = att_info['subject_timetable_id']
        latitude  = att_info['latitude']
        longitude = att_info['longitude']
        
        id             = request.user.id #5
        classroom      = request.user.classroom #CS-ROOM-02
        day            = datetime.now().date().strftime("%A") #Sunday

        subjects = Timetable.objects.filter(classroom_id=classroom,day=day)
        subject_id = Timetable.objects.get(classroom=classroom,day=day,id=subject_timetable_id).subject.id

        module = Timetable.objects.get(classroom=classroom,day=day,id=subject_timetable_id).subject.subject.module_no

        subject_start_time = Timetable.objects.get(classroom=classroom,day=day,id=subject_timetable_id).start_time
        strt = time.strptime(subject_start_time, '%I:%M%p')
        subject_start_time = time.strftime('%H:%M', strt)
        subject_start_time = datetime.strptime(subject_start_time,"%H:%M").time()
            
        sub_time_obj = datetime.combine(date.today(),subject_start_time)
        
        now = datetime.now().strftime("%H:%M:%S")

        x = Attendance.objects.filter(student_id=id,classroom_id=classroom,subject_id=subject_timetable_id,date=datetime.now().strftime("%Y-%m-%d"))
        #x = Attendance.objects.filter(student_id=6,classroom_id="CS02",subject_id=9,date="2021-06-29")
        #print(f"x : {x}")
        if not x:
            #print("Student didn't take his attendance for this class.We must allow this function to continue.")
            already_exist = True
        else:
            #print("student already taken attendance for this class.")
            already_exist = False

        if late(sub_time_obj) & is_in_class(latitude,longitude,classroom) & already_exist : 
            print("added attendance successfully, we will return 200 response.")
            print(f"id : {id} , classroom : {classroom} , subject_id {subject_id}")

            Attendance.objects.create(student_id=id,classroom_id=classroom,subject_id=subject_timetable_id,time=now,date=datetime.now().strftime("%Y-%m-%d"))
            #Attendance.objects.create(student_id=10,classroom_id="CS-ROOM-02",subject_id=27,date="2021-06-29",time="16:21:20")
            return JsonResponse({'foo':'bar'},status=200)
        else:
            print("Student may be late/outside of the class/already attended.we will return 4xx response.")
            return JsonResponse({"msg":"You late"},status=403)

    else:
        return render(request,'attendance_system/error.html',{'msg':'Method not allowed.'})

@login_required
def percent(request):
    if request.user.is_authenticated:
        print("logged in.")

        id = request.user.id
        classroom = request.user.classroom

        class_sub_ids = ClassroomSubject.objects.filter(class_id_id=classroom)
        class_sub_id_list = [s.id for s in class_sub_ids] #[11, 12, 13, 14, 15, 16]
        
        class_module_no_in_list = [s.subject_id for s in class_sub_ids] #['CS-2101', 'CS-2102', 'CS-2103', 'CS-2104', 'CS-2105', 'ENG-2001']
        module_no_per_month = {}

        for i in class_module_no_in_list:
            module_no_per_month[i] = (Timetable.objects.filter(subject_id__subject_id=i).count()) * 4
            #output
            '''
            {'CS-2101': 12,
            'CS-2102': 12,
            'CS-2103': 12,
            'CS-2104': 8,
            'CS-2105': 8,
            'ENG-2001': 12}
            '''
        aa = Attendance.objects.filter(student_id=id,classroom_id=classroom)
        total_attended_module_no_list = [s.subject.subject.subject.module_no for s in aa]
        total_attended_module_no = {}
        for i in total_attended_module_no_list:
            total_attended_module_no[i] = total_attended_module_no_list.count(i)

            
        not_exist = []
        for x in module_no_per_month:
            if x not in total_attended_module_no:
                not_exist.append(x)
            
        print(not_exist)
        for i in not_exist:
            module_no_per_month.pop(i)

        def sort(x):
            sorted_dict = {}
            sorted_keys = sorted(x.keys())

            for i in sorted_keys:
                sorted_dict[i] = x[i]
            return sorted_dict
        
        sorted_module_no_per_month = sort(module_no_per_month)
        sorted_total_attended_module_no = sort(total_attended_module_no)

        #print('sorted_module_no_per_month',sorted_module_no_per_month)
        #print('sorted_total_attended_module_no',sorted_total_attended_module_no)

        #print( ( 5/10 ) * 100 )

        res = { key : round((total_attended_module_no[key] / module_no_per_month.get(key, 0))*100,2) for key in module_no_per_month.keys() }
        for i in not_exist:
            res[i] = 0

        print(res)

        return JsonResponse(res,status=200)
    else:
        print("Not logged in.")

    return render(request,'attendance_system/index.html')

