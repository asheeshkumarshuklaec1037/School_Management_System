from django.shortcuts import render,redirect
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth.views import LoginView


def home_view(request):
    messages=models.DisplayMessage.objects.all()
    address=models.Address.objects.first()
    toppers=models.Topper.objects.all()
    return render(request,'school/index.html',{'messages':messages,'toppers':toppers,'address':address})



#for showing login button for teacher
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/adminclick.html')


#for showing login button for teacher
def teacherclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/teacherclick.html')


#for showing login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'school/studentclick.html')


#for checking user is teacher, student or admin
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_teacher(request.user):
        return redirect('teacher-dashboard')
    elif is_student(request.user):
        return redirect('student-dashboard')
    

# Creating custom login to show error message if incorrect username or password
class CustomLoginView(LoginView):
    def form_invalid(self, form):
        messages.error(self.request, 'Incorrect username or password. Please try again.')
        return super().form_invalid(form)

#for admin dashboard 
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=models.TeacherExtra.objects.all().count()
    studentcount=models.StudentExtra.objects.all().count()
    teachersalary=models.TeacherExtra.objects.all().aggregate(Sum('salary',default=0))
    studentfee=models.StudentExtra.objects.all().aggregate(Sum('fee',default=0))
    notice=models.Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,
        'studentcount':studentcount,
        'teachersalary':teachersalary['salary__sum'],
        'studentfee':studentfee['fee__sum'],
        'notice':notice,
    }
    return render(request,'school/admin_dashboard.html',context=mydict)


@login_required(login_url='login')
@user_passes_test(is_admin)
def update_admin_view(request):
    user=request.user
    form=forms.AdminUpdateForm(instance=user)
    mydict={'form':form}
    if request.method=='POST':
        form=forms.AdminUpdateForm(request.POST,instance=user)
        if form.is_valid():
            user=form.save()
            password = form.cleaned_data['password']
            if password:
                user.password = make_password(password)
            user.save()
            return redirect('logout')
    return render(request,'school/admin_update.html',context=mydict)

#for teacher section by admin
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'school/admin_teacher.html')

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=forms.TeacherUserForm()
    form2=forms.TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST)
        form2=forms.TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-teacher')
    return render(request,'school/admin_add_teacher.html',context=mydict)


@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=models.TeacherExtra.objects.all()
    return render(request,'school/admin_view_teacher.html',{'teachers':teachers})


@login_required(login_url='login')
@user_passes_test(is_admin)
def update_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)

    form1=forms.TeacherUserForm(instance=user)
    form2=forms.TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=forms.TeacherUserForm(request.POST,instance=user)
        form2=forms.TeacherExtraForm(request.POST,instance=teacher)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            password = form1.cleaned_data['password']
            if password:
                user.password = make_password(password)
            user.save()
            f2=form2.save(commit=False)
            f2.save()
            messages.success(request, 'Teacher details updated successfully.')
            return redirect('admin-view-teacher')
        else:
            messages.error(request, 'Failed to update teacher details. Please check the form fields.')
            return redirect('admin-view-teacher')
    return render(request,'school/admin_update_teacher.html',context=mydict)


@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=models.TeacherExtra.objects.get(id=pk)
    user=models.User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-view-teacher')


#for student section by admin
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'school/admin_student.html')

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=forms.StudentUserForm()
    form2=forms.StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST)
        form2=forms.StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'school/admin_add_student.html',context=mydict)

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_class_view(request):
    students1=models.StudentExtra.objects.filter(cl='one').count()
    students2=models.StudentExtra.objects.filter(cl='two').count()
    students3=models.StudentExtra.objects.filter(cl='three').count()
    students4=models.StudentExtra.objects.filter(cl='four').count()
    students5=models.StudentExtra.objects.filter(cl='five').count()
    students6=models.StudentExtra.objects.filter(cl='six').count()
    students7=models.StudentExtra.objects.filter(cl='seven').count()
    students8=models.StudentExtra.objects.filter(cl='eight').count()
    students9=models.StudentExtra.objects.filter(cl='nine').count()
    students10=models.StudentExtra.objects.filter(cl='ten').count()
    context={
        'student1':students1,
        'student2':students2,
        'student3':students3,
        'student4':students4,
        'student5':students5,
        'student6':students6,
        'student7':students7,
        'student8':students8,
        'student9':students9,
        'student10':students10,
    }
    return render(request,'school/admin_view_class.html',context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_student_view(request,cl):
    students=models.StudentExtra.objects.filter(cl=cl)
    return render(request,'school/admin_view_student.html',{'students':students})

@login_required(login_url='login')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    form1=forms.StudentUserForm(instance=user)
    form2=forms.StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=forms.StudentUserForm(request.POST,instance=user)
        form2=forms.StudentExtraForm(request.POST,instance=student)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            password = form1.cleaned_data['password']
            if password:
                user.password = make_password(password)
            user.save()
            f2=form2.save(commit=False)
            f2.save()
            return redirect('admin-student')
    return render(request,'school/admin_update_student.html',context=mydict)

@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_student_view(request,pk):
    student=models.StudentExtra.objects.get(id=pk)
    user=models.User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('admin-view-student')


#attendance related view
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'school/admin_attendance.html')

@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,cl):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=models.Attendance.objects.filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/admin_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/admin_view_attendance_ask_date.html',{'cl':cl,'form':form})


#fee related view by admin
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_view_class_total_fee(request):
    studentfee1=models.StudentExtra.objects.filter(cl='one').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee2=models.StudentExtra.objects.filter(cl='two').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee3=models.StudentExtra.objects.filter(cl='three').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee4=models.StudentExtra.objects.filter(cl='four').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee5=models.StudentExtra.objects.filter(cl='five').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee6=models.StudentExtra.objects.filter(cl='six').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee7=models.StudentExtra.objects.filter(cl='seven').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee8=models.StudentExtra.objects.filter(cl='eight').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee9=models.StudentExtra.objects.filter(cl='nine').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee10=models.StudentExtra.objects.filter(cl='ten').aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    studentfee=models.StudentExtra.objects.all().aggregate(Sum('fee',default=0)).get('fee__sum', 0)
    context={
        'studentfee1':studentfee1,
        'studentfee2':studentfee2,
        'studentfee3':studentfee3,
        'studentfee4':studentfee4,
        'studentfee5':studentfee5,
        'studentfee6':studentfee6,
        'studentfee7':studentfee7,
        'studentfee8':studentfee8,
        'studentfee9':studentfee9,
        'studentfee10':studentfee10,
        'studentfee':studentfee
    }
    return render(request,'school/admin_view_class_total_fee.html',context)


#notice related views
@login_required(login_url='login')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name+" "+request.user.last_name
            form.save()
            return redirect('admin-notice')
    notices=models.Notice.objects.filter(by=request.user.first_name+" "+request.user.last_name)
    return render(request,'school/admin_notice.html',{'form':form, 'notices':notices})

@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_admin_notice_view(request,pk):
    notice=models.Notice.objects.get(id=pk)
    notice.delete()
    return redirect('admin-notice')


# Messsages from public related views
def contact_us(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        contact=request.POST.get('contact')
        address=request.POST.get('address')
        message=request.POST.get('message')
        contactus=models.ContactUs(name=name, email=email, contact=contact, address=address, message=message)
        contactus.save()
        return redirect('/')
    return render(request,'school/index.html')

@login_required(login_url='login')
@user_passes_test(is_admin)    
def message(request):
    messages=models.ContactUs.objects.all()
    mydict={
        'messages':messages
    }
    return render(request, 'school/messages.html', context=mydict)

@login_required(login_url='login')
@user_passes_test(is_admin)    
def view_messages(request, pk):
    message=models.ContactUs.objects.get(id=pk)
    mydict={
        'message':message
    }
    return render(request, 'school/view_messages.html', context=mydict)

@login_required(login_url='login')
@user_passes_test(is_admin) 
def delete_message(request,pk):
    message=models.ContactUs.objects.get(id=pk)
    message.delete()
    return redirect('messages')

# Display message on homepage related views
@login_required(login_url='login')
@user_passes_test(is_admin)
def add_display_message(request):
    if request.method=='POST':
        form=forms.DisplayMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add-display-message')
    form=forms.DisplayMessageForm()
    messages=models.DisplayMessage.objects.all()
    return render(request, 'school/add_display_message.html', {'messages':messages,'form':form})

@login_required(login_url='login')
@user_passes_test(is_admin)
def edit_display_message(request,pk):
    data=models.DisplayMessage.objects.get(id=pk)
    if request.method=='POST':
        form=forms.DisplayMessageForm(request.POST, instance=data)
        if form.is_valid():
            form=form.save(commit=False)
            form.save()
            return redirect('add-display-message')
    form=forms.DisplayMessageForm(request.POST, instance=data)
    return render(request,'school/edit_display_message.html',{'form':form})

@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_display_message(request,pk):
    message=models.DisplayMessage.objects.get(id=pk)
    message.delete()
    return redirect('add-display-message')


# Display toppers on homepage related views
@login_required(login_url='login')
@user_passes_test(is_admin)
def add_topper_list(request):
    if request.method=='POST':
        form=forms.TopperForm(request.POST, request.FILES)
        if form.is_valid():
            form=form.save(commit=False)
            form.save()
            return redirect('add-topper-list')
        print(form.errors)
    form=forms.TopperForm(request.POST, request.FILES)
    toppers=models.Topper.objects.all()
    context={
        'form':form,
        'toppers':toppers
    }
    return render(request,'school/add_topper_list.html',context)

@login_required(login_url='login')
@user_passes_test(is_admin)
def update_topper(request, pk):
    topper=models.Topper.objects.get(id=pk)
    form=forms.TopperForm(instance=topper)
    mydict={'form':form}

    if request.method=='POST':
        form=forms.TopperForm(request.POST, request.FILES ,instance=topper)
        if form.is_valid():
            topper=form.save()
            return redirect('add-topper-list')
    return render(request,'school/update_topper.html',context=mydict)

@login_required(login_url='login')
@user_passes_test(is_admin)
def delete_topper(request,pk):
    topper=models.Topper.objects.get(id=pk)
    topper.delete()
    return redirect('add-topper-list')


# Display address on homepage related views
@login_required(login_url='login')
@user_passes_test(is_admin)
def display_address(request):
    address=models.Address.objects.all()
    return render(request, 'school/display_address.html', {'address':address})

@login_required(login_url='login')
@user_passes_test(is_admin)
def edit_display_address(request):
    data=models.Address.objects.first()
    print(data)
    if request.method=='POST':
        form=forms.AddressForm(request.POST, instance=data)
        if form.is_valid():
            form=form.save(commit=False)
            form.save()
            return redirect('display-address')
    form=forms.AddressForm(initial={
            'area': data.area,
            'district': data.district,
            'state': data.state,
            'pin': data.pin,
            'mobile': data.mobile,
            'email': data.email,
        })
    return render(request,'school/edit_display_address.html',{'form':form})

#For teacher dashboard
@login_required(login_url='login')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=models.TeacherExtra.objects.filter(user=request.user)
    notice=models.Notice.objects.all()
    mydict={
        'salary':teacherdata[0].salary,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice,
        'class':teacherdata[0].cl
    }
    return render(request,'school/teacher_dashboard.html',context=mydict)


# Teacher attendance related views
@login_required(login_url='login') 
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    teacher=models.TeacherExtra.objects.get(user=request.user)
    cl=teacher.cl
    return render(request,'school/teacher_attendance.html',{'cl':cl})

@login_required(login_url='login')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request):
    teacher=models.TeacherExtra.objects.get(user=request.user)
    cl=teacher.cl
    students=models.StudentExtra.objects.filter(cl=cl)
    aform=forms.AttendanceForm()
    if request.method=='POST':
        form=forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            existing_attendance = models.Attendance.objects.filter(cl=cl, date=date)
            
            if existing_attendance.exists():
                # Update the existing attendance records
                for i, attendance in enumerate(existing_attendance):
                    attendance.present_status = Attendances[i]
                    attendance.save()
            else:
                for i in range(len(Attendances)):
                    AttendanceModel=models.Attendance()
                    AttendanceModel.cl=cl
                    AttendanceModel.date=date
                    AttendanceModel.present_status=Attendances[i]
                    AttendanceModel.roll=students[i].roll
                    AttendanceModel.save()
                return redirect('teacher-attendance')
        else:
            print('form invalid')
    return render(request,'school/teacher_take_attendance.html',{'students':students,'aform':aform})

@login_required(login_url='login')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request):
    teacher=models.TeacherExtra.objects.get(user=request.user)
    cl=teacher.cl
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date'] 
            attendancedata=models.Attendance.objects.filter(date=date,cl=cl)
            studentdata=models.StudentExtra.objects.filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/teacher_view_attendance_page.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/teacher_view_attendance_ask_date.html',{'cl':cl,'form':form})

# Teacher notice related views
@login_required(login_url='login')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=forms.NoticeForm()
    if request.method=='POST':
        form=forms.NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name+" "+request.user.last_name
            form.save()
            return redirect('teacher-notice')
        else:
            print('form invalid')
    notices=models.Notice.objects.filter(by=request.user.first_name+" "+request.user.last_name)
    return render(request,'school/teacher_notice.html',{'form':form, 'notices':notices})

@login_required(login_url='login')
@user_passes_test(is_teacher)
def delete_teacher_notice_view(request,pk):
    notice=models.Notice.objects.get(id=pk)
    notice.delete()
    return redirect('teacher-notice')


# For student dashboard
@login_required(login_url='login')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=models.StudentExtra.objects.filter(user=request.user)
    notice=models.Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'class':studentdata[0].cl,
        'notice':notice
    }
    return render(request,'school/student_dashboard.html',context=mydict)

#  For student attendance
@login_required(login_url='login')
@user_passes_test(is_student)
def student_attendance_view(request):
    form=forms.AskDateForm()
    if request.method=='POST':
        form=forms.AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            studentdata=models.StudentExtra.objects.filter(user_id=request.user.id)
            attendancedata=models.Attendance.objects.filter(date=date,cl=studentdata[0].cl,roll=studentdata[0].roll)
            mylist=zip(attendancedata,studentdata)
            return render(request,'school/student_view_attendance_page.html',{'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'school/student_view_attendance_ask_date.html',{'form':form})


# About developer related view
def about_developer(request):
    return render(request,'school/about_developer.html')