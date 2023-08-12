from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.

classes=[('one','one'),('two','two'),('three','three'),
('four','four'),('five','five'),('six','six'),('seven','seven'),('eight','eight'),('nine','nine'),('ten','ten')]
class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=10)
    mobile = models.CharField(max_length=40,null=True)
    fee=models.PositiveIntegerField(null=True)
    cl= models.CharField(max_length=10,choices=classes,default='one')
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(null=False)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    cl= models.CharField(max_length=10,choices=classes,default='one')
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name


class Attendance(models.Model):
    roll=models.CharField(max_length=10,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=10)
    present_status= models.CharField(max_length=10)


class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='school')
    message=models.CharField(max_length=500)

class ContactUs(models.Model):
    date=models.DateField(auto_now=True)
    name=models.CharField(max_length=50, null=False)
    email=models.EmailField(max_length=50, null=False)
    contact=models.IntegerField(max_length=13, null=False)
    address=models.CharField(max_length=100, default='')
    message=models.CharField(max_length=500, null=False)

class DisplayMessage(models.Model):
    message=models.CharField(max_length=1000)

class Topper(models.Model):
    name = models.CharField(max_length=100)
    class_name = models.IntegerField()
    year = models.IntegerField()
    photo = models.ImageField(upload_to='images/student')
    marks= models.IntegerField(default=0)
    total_marks= models.IntegerField(default=500)
    percentage=models.FloatField(default=0.00)
    
@receiver(pre_delete, sender=Topper)
def delete_student_image(sender, instance, **kwargs):
# Delete the associated image file
    instance.photo.delete(save=False)

class Address(models.Model):
    area=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pin=models.IntegerField()
    mobile=models.IntegerField()
    email=models.EmailField(max_length=50)
