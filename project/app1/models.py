from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class LoginUser(AbstractUser):

    statuschoices=(('APPROVE','APPROVE'),
                   ('REJECT','REJECT'),
                   )
    status=models.CharField(choices=statuschoices,max_length=20,default='PENDING',null=True,blank=True)
    user_type=models.CharField(max_length=50)

class User(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    user_name=models.CharField(max_length=20)
    street=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    pincode=models.IntegerField()
    Email=models.EmailField()
    phone=models.IntegerField()

    def __str__(self):
        return self.user_name

# class Seller(models.Model):
#     login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
#     seller_name=models.CharField(max_length=20)
#     street=models.CharField(max_length=50)
#     district=models.CharField(max_length=50)
#     pincode=models.IntegerField()    
#     Email=models.EmailField()
#     phone=models.IntegerField()

#     def __str__(self):
#         return self.seller_name
    

class Product(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    product_name=models.CharField(max_length=30)
    price=models.IntegerField()
    product_details=models.CharField(max_length=100)
    location=models.CharField(max_length=30)
    image1=models.FileField(upload_to='product')
    image2=models.FileField(upload_to='product')
    image3=models.FileField(upload_to='product')





class Hospital(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    hospital_name=models.CharField(max_length=20)
    street=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    pincode=models.IntegerField()
    Email=models.EmailField()
    phone=models.IntegerField()
    licence_proof=models.FileField(upload_to='licence')

    def __str__(self):
        return self.hospital_name

class Parent(models.Model):
    login_id=models.ForeignKey(LoginUser,on_delete=models.CASCADE)
    hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    parent_name=models.CharField(max_length=20)
    street=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    pincode=models.IntegerField()
    Email=models.EmailField()
    phone=models.IntegerField()
    baby_status=models.CharField(max_length=50,null=True, blank=True,)
    def __str__(self):
        return self.parent_name
    
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
    consulting_time=models.TimeField()
    slots=models.IntegerField()
    availability_status=models.CharField(max_length=10,default="AVAILABLE")

class Booking(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    parent_id=models.ForeignKey(Parent,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now=True)
    booking_date = models.DateField()
    token_number = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


    @classmethod
    def get_next_token(cls, doctor_id,parent_id, booking_date):
        # Get the highest token number for the given doctor and booking date
        last_token = cls.objects.filter(doctor_id=doctor_id, booking_date=booking_date).order_by('-token_number').first()

        if last_token:
            # If tokens exist for the given doctor and booking date, increment the last token number
            next_token_number = last_token.token_number + 1
        else:
            # If no tokens exist for the given doctor and booking date, start from 1
            next_token_number = 1


        return next_token_number

class Vaccination(models.Model):
     hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
     Vaccination_name=models.CharField(max_length=100,blank=True,null=True)
     Dose=models.IntegerField(null=True, blank=True)
     Age=models.IntegerField(null=True, blank=True)
     days=models.IntegerField(null=True,blank=True)
     
     def __str__(self):
        return self.Vaccination_name
     



class Baby_details(models.Model):
    parent_id=models.ForeignKey(Parent,on_delete=models.CASCADE)
    hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
    baby_name=models.CharField(max_length=20)
    father_name=models.CharField(max_length=20,null=True,blank=True)
    gender=models.CharField(max_length=20,null=True,blank=True)
    blood_group=models.CharField(max_length=20,null=True,blank=True)
    weight=models.IntegerField()
    birth_date=models.DateField()
    def __str__(self):
        return self.baby_name

class Baby_vaccine(models.Model):
    baby_id=models.ForeignKey(Baby_details,on_delete=models.CASCADE)
    vaccination_id=models.ForeignKey(Vaccination,on_delete=models.CASCADE,null=True, blank=True)
    vaccination_status=models.CharField(max_length=50,null=True, blank=True)
    date=models.DateField(null=True,blank=True)


class Productbooking(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    parent_id=models.ForeignKey(Parent,on_delete=models.CASCADE,null=True, blank=True)
    date=models.DateField(auto_now=True)
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    status=models.CharField(max_length=15,default="pending")


class Cart(models.Model):
    product_id=models.ForeignKey(Product,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    parent_id=models.ForeignKey(Parent,on_delete=models.CASCADE,null=True, blank=True)
    date=models.DateField(auto_now=True)


class Chat(models.Model):
    sender=models.ForeignKey(LoginUser,on_delete=models.CASCADE,related_name="send_messages")  
    receiver=models.ForeignKey(LoginUser,on_delete=models.CASCADE,related_name="received_messages")    
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.message}"

class Video(models.Model):
     hospital_id=models.ForeignKey(Hospital,on_delete=models.CASCADE)
     title=models.CharField(max_length=30)
     discription=models.CharField(max_length=100,null=True, blank=True)
     upload_date=models.DateField(auto_now=True)
     video=models.FileField(upload_to='videos')

class VaccineDocument(models.Model):
    parent_id=models.ForeignKey(Parent,on_delete=models.CASCADE)
    vaccination_id=models.ForeignKey(Vaccination,on_delete=models.CASCADE)
    hospital_name=models.CharField(max_length=40)
    document=models.FileField(upload_to='document')
    




    