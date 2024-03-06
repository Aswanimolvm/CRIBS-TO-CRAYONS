from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class LoginUser(AbstractUser):
    statuschoices=(('APPROVE','APPROVE'),
                   ('REJECT','REJECT'),
                   ('PENDING','PENDING'))
    status=models.CharField(choices=statuschoices,max_length=20,default='PENDING',null=True,blank=True)
    user_type=models.CharField(max_length=50)

class Customer(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    Customer_name=models.CharField(max_length=20)
    Address=models.CharField(max_length=50)
    Email=models.EmailField()
    phone=models.IntegerField()

    def __str__(self):
        return self.Customer_name

class Seller(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    seller_name=models.CharField(max_length=20)
    Address=models.CharField(max_length=50)
    Email=models.EmailField()
    phone=models.IntegerField()

    def __str__(self):
        return self.seller_name

class Hospital(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    hospital_name=models.CharField(max_length=20)
    Address=models.CharField(max_length=50)
    Email=models.EmailField()
    phone=models.IntegerField()
    licence_proof=models.FileField(upload_to='licence')

    def __str__(self):
        return self.hospital_name

class Parent(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    parent_name=models.CharField(max_length=20)
    Address=models.CharField(max_length=50)
    Email=models.EmailField()
    phone=models.IntegerField()
    blood_group=models.CharField(max_length=10)
    baby_status=models.CharField(max_length=50,null=True, blank=True,)
    
class Nutritionist(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    Nutritionist_name=models.CharField(max_length=20)
    hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    consulting_days=models.CharField(max_length=100)
    consulting_time=models.CharField(max_length=100)

class Doctor(models.Model):
    hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    Doctor_name=models.CharField(max_length=20)
    qualification=models.CharField(max_length=50)
    department=models.CharField(max_length=20)
    consulting_days=models.CharField(max_length=30)
    slots=models.IntegerField()
    availability_status=models.CharField(max_length=10,default="AVAILABLE")

class Booking(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    parent_id=models.ForeignKey(Parent,on_delete=models.CASCADE)
    booking_date=models.CharField(max_length=10)
    booking_time=models.TimeField(auto_now=True)

class Vaccination(models.Model):
     hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
     Vaccination_name=models.CharField(max_length=100,blank=True,null=True)
     duration=models.IntegerField(null=True, blank=True)
     

class Baby_details(models.Model):
    parent_id=models.ForeignKey(Parent,on_delete=models.CASCADE)
    hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    baby_name=models.CharField(max_length=20)
    father_name=models.CharField(max_length=20,null=True,blank=True)
    gender=models.CharField(max_length=20,null=True,blank=True)
    blood_group=models.CharField(max_length=20,null=True,blank=True)
    weight=models.IntegerField()
    birth_date=models.DateField()
    

class Baby_vaccine(models.Model):
    baby_id=models.ForeignKey(Baby_details,on_delete=models.CASCADE)
    vaccination_id=models.ForeignKey(Vaccination,on_delete=models.CASCADE,null=True, blank=True)
    vaccination_status=models.CharField(max_length=50,null=True, blank=True,)
    date=models.DateField(null=True,blank=True)


class Product(models.Model):
    seller_id=models.ForeignKey(Seller,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=30)
    price=models.IntegerField()
    product_details=models.CharField(max_length=100)
    location=models.CharField(max_length=30)
    image=models.FileField(upload_to='product')


class Video(models.Model):
     hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
     title=models.CharField(max_length=30)
     upload_date=models.DateField()
     video=models.FileField(upload_to='videos')




class Chat(models.Model):
    Seller_id=models.ForeignKey(Seller,on_delete=models.CASCADE)  
    Customer_id=models.ForeignKey(Customer,on_delete=models.CASCADE)    
    message=models.CharField(max_length=250,null=True,blank=True)



    