from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import User

class StudentRegisterForm(UserCreationForm):

    ATTENDING_YEAR = [

        ('FirstYear','FirstYear'),
        ('SecondYear','SecondYear'),
        ('ThirdYear','ThirdYear'),
        ('FourthYear','FourthYear')
    ]
    
    ROLL_NO_PREFIX = [

        ('1KaTha/','1kaTha/'),
        ('2KaTha/','2KaTha/'),
        ('3KaTha/','3KaTha/'),
        ('4KaTha/','4KaTha/')
    ]

    email = forms.EmailField()
    attending_year = forms.ChoiceField(choices = ATTENDING_YEAR)
    roll_no_prefix = forms.ChoiceField(choices = ROLL_NO_PREFIX)
    roll_no_number = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','attending_year','roll_no_prefix','roll_no_number','password1','password2')
    
