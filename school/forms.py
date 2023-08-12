from django import forms
from django.contrib.auth.models import User
from . import models

#for admin
class AdminUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password','email']


#for teacher
class TeacherUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class TeacherExtraForm(forms.ModelForm):
    class Meta:
        model=models.TeacherExtra
        fields=['salary','mobile','cl']
        

#for student 
class StudentUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
class StudentExtraForm(forms.ModelForm):
    class Meta:
        model=models.StudentExtra
        fields=['roll','cl','mobile','fee']


#for Attendance 
presence_choices=(('Present','Present'),('Absent','Absent'))
class AttendanceForm(forms.Form):
    present_status=forms.ChoiceField( choices=presence_choices)
    date=forms.DateField()

class AskDateForm(forms.Form):
    date=forms.DateField()

#for notice 
class NoticeForm(forms.ModelForm):
    class Meta:
        model=models.Notice
        fields='__all__'


#for display message 
class DisplayMessageForm(forms.ModelForm):
    class Meta:
        model=models.DisplayMessage
        fields='__all__'


# for topper page
class TopperForm(forms.ModelForm):
    class Meta:
        model=models.Topper
        fields='__all__'


# for address page
class AddressForm(forms.ModelForm):
    class Meta:
        model=models.Address
        fields='__all__'


