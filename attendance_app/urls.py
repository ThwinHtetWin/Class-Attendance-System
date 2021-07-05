from django.urls import path

from . import views
from .views import StudentRegisterView
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('register/',views.StudentRegisterView,name='register'),
    path('timetable/',views.timetable,name='timetable'),
    path('attendance/',views.attendance,name='attendance'),
    path('enrollment/',views.enrollment,name='enrollment'),
    path('add_attendance/',views.add_attendance,name="add_attendance"),
    path('percent/',views.percent,name='percent')

]