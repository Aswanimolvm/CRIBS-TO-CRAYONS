from django.shortcuts import render,redirect
from .models import Seller,Customer,Hospital,LoginUser,Parent,Nutritionist,Baby_details,Product
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'Home/home.html')
def seller_register(request):
    if request.method=='POST':
        seller_name=request.POST['seller_name']
        address=request.POST['address']
        phone_number=request.POST['phone']
        email=request.POST['email']
        password=request.POST['password']    
        password2=request.POST['confirmPassword'] 
        if password != password2:
            return render(request,'Home/sreg.html',{'message':"password doesn't match"})   
        login_data=LoginUser.objects.create_user(username=seller_name,password=password,user_type='seller')
        login_data.save()
        log_id=LoginUser.objects.get(id=login_data.id)
        seller_data=Seller.objects.create(login_id=log_id,seller_name=seller_name,Address=address,Email=email,phone=phone_number)
        seller_data.save()
        return redirect(loginpage)      
    else:
        return render(request,'Home/sreg.html')
def customer_register(request):
    if request.method=='POST':
        customer_name=request.POST['Customer_name']
        address=request.POST['Address']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        password=request.POST['password']
        password1=request.POST['confirmPassword']
        if password != password1:
            return render(request,'Home/creg.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=customer_name,password=password,user_type='customer')
        login_data.save()
        log_id=LoginUser.objects.get(id=login_data.id)
        customer_data=Customer.objects.create(login_id=log_id,Customer_name=customer_name,Address=address,Email=email,phone=phone_number)
        customer_data.save()
        return redirect(loginpage)
    else:
        return render(request,'Home/creg.html')

    # return render(request,'Home/creg.html')
def hospital_register(request):
    if request.method=='POST':
        hospital_name=request.POST['hospital_name']
        address=request.POST['Address']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        licence_proof=request.FILES['licence_proof']
        password=request.POST['password']
        password2=request.POST['confirmPassword']
        if password != password2:
            return render(request,'Home/hreg.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=hospital_name,password=password,user_type="hospital")
        login_data.save()
        log_id=LoginUser.objects.get(id=login_data.id)
        hospital_data=Hospital.objects.create(login_id=log_id,hospital_name=hospital_name,Address=address,Email=email,phone=phone_number,licence_proof=licence_proof)
        hospital_data.save()
        return redirect(loginpage)
    else:
        return render(request,'Home/hreg.html')
    

def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        data=authenticate(username=username,password=password)
        if data is not None:
            login(request,data)
            if data.user_type=="seller" and data.status=="APPROVE":
                return redirect(seller_profile)
            elif data.user_type=="customer" and data.status=="APPROVE":
                return redirect(customer_profile)
            elif data.user_type=="hospital" and data.status=="APPROVE":
                return redirect(hospital_profile)
            elif data.user_type=="parent":
                return redirect(parent_profile)
            elif data.user_type=="nutritionist":
                return redirect(n_profile)
            else:
                return render(request,'Home/login.html',{'message':"please wait for the approval"})
        else:
            return render(request,'Home/login.html',{'message':"invalid credential"})

    else:
        return render(request,'Home/login.html')










def hospital_profile(request):
    return render(request,'Hospital/hospitalprofile.html')

def about(request):
    return render(request,'Home/about.html')
def edit_hospital(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    if request.method=='POST':
        hospital_name=request.POST['hospital_name']
        address=request.POST['Address']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        hospital.hospital_name = hospital_name
        hospital.Address=address
        hospital.Email=email
        hospital.phone=phone_number
        hospital.save()
        log_id.username=hospital_name
        log_id.save()
        return HttpResponse("updated")
    else:
        return render(request,'Hospital/edithprofile.html',{'hospital':hospital})
def add_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital_id=Hospital.objects.get(login_id=log_id)
    if request.method=='POST':
        parent_name=request.POST['parent_name']
        address=request.POST['Address']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        blood_group=request.POST['blood_group']
        password=request.POST['password']
        password2=request.POST['confirmPassword']
        if password != password2:
            return render(request,'Hospital/addparent.html',{'message':"password doesn't match"})
        
        login_data=LoginUser.objects.create_user(username=parent_name,password=password,user_type="parent")
        login_data.save()
        logg_id=LoginUser.objects.get(id=login_data.id)
        parent_data=Parent.objects.create(
                                        login_id=logg_id,
                                        hospital_id=hospital_id,
                                        parent_name=parent_name,
                                        Address=address,
                                        Email=email,
                                        phone=phone_number,
                                        blood_group=blood_group
                                        )
        parent_data.save()
        return render(request,'Hospital/addparent.html',{'message':"PARENT ADDED"})
    else:
        return render(request,'Hospital/addparent.html')
def add_baby(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    parent=Parent.objects.get(id=id)
    
    if request.method=='POST':
        baby_name=request.POST['baby_name']
        father_name=request.POST['father_name']
        birth_date=request.POST['birth_date']
        gender=request.POST['gender']
        weight=request.POST['weight']
        blood_group=request.POST['blood_group']
        baby_data=Baby_details.objects.create(baby_name=baby_name,
                                              hospital_id=hospital,
                                              parent_id=parent,
                                              father_name=father_name,
                                              birth_date=birth_date,
                                              gender=gender,
                                              weight=weight,
                                              blood_group=blood_group,)
        baby_data.save()
        parent.baby_status="True"
        parent.save()
        return render(request,'Hospital/addbaby.html',{'message':"Successfully Added",'parent':parent})
    else:
        return render(request,'Hospital/addbaby.html',{'parent':parent})
def view_baby(request,id):
    parent=Parent.objects.get(id=id)
    baby=Baby_details.objects.filter(parent_id=parent)
    print(baby)
    context={
        'baby':baby
    }

    return render(request,'Hospital/viewbabydetails.html',context)    

def add_nutritionist(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital_id=Hospital.objects.get(login_id=log_id)
    if request.method=='POST':
        nutritionist_name=request.POST['Nutritionist_name']
        consulting_days=request.POST['consulting_days']
        consulting_time=request.POST['consulting_time']
        password=request.POST['password']
        password1=request.POST['confirmPassword']
        if password != password1:
            return render(request,'Hospital/addnutritionist.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=nutritionist_name,password=password,user_type="nutritionist")
        login_data.save()
        logg_id=LoginUser.objects.get(id=login_data.id)
        nutritionist_data=Nutritionist.objects.create(login_id=logg_id,
                                                      hospital_id=hospital_id,
                                                      Nutritionist_name=nutritionist_name,
                                                      consulting_days=consulting_days,
                                                      consulting_time=consulting_time
                                                      )
        nutritionist_data.save()
        return render(request,'Hospital/addnutritionist.html',{'message':"Successfully Added"})
    else:
         return render(request,'Hospital/addnutritionist.html')

def parent_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    context={
        'parent':parent
    }
    return render(request,'Parent/parentprofile.html',context)
def baby_details(request,id):
     parent=LoginUser.objects.get(id=request.user.id)
     baby=Baby_details.objects.filter(parent_id=parent)
     print(baby)
     context={
        'baby':baby
     }

     return render(request,'Parent/babydetails.html',context)
def edit_baby(request):
    return render(request,'Parent/editbabydetails.html')
def edit_parent(request):
    return render(request,'Parent/editparent.html')
def add_doctor_details(request):
    return render(request,'Hospital/adddoctordetails.html')
def view_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital_id=Hospital.objects.get(login_id=log_id)
    parents=Parent.objects.filter(hospital_id=hospital_id)
    context={
        'parent': parents
    }
    return render(request,'Hospital/viewparents.html',context)
def edit_doctor(request):
    return render(request,'Hospital/editdoctor.html')


def seller_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    seller=Seller.objects.get(login_id=log_id)
    context={
        'seller':seller
    }
    return render(request,'Seller/sellerprofile.html',context)
def add_product(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    seller_id=Seller.objects.get(login_id=log_id)
    if request.method=='POST':
        product_name=request.POST['product_name']
        price=request.POST['price']
        product_details=request.POST['product_details']
        location=request.POST['location']
        image=request.FILES['image']
        product_data=Product.objects.create(seller_id=seller_id,
                                            product_name=product_name,
                                            price=price,
                                            product_details=product_details,
                                            location=location,
                                            image=image)
        product_data.save()
        return render(request,'Seller/addproducts.html',{'message':"successfully uploaded!!"})
    return render(request,'Seller/addproducts.html')
def edit_product(request):
    return render(request,'Seller/editproduct.html')
def edit_seller(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    seller=Seller.objects.get(login_id=log_id)
    if request.method=='POST':
        seller_name=request.POST['seller_name']
        address=request.POST['address']
        phone_number=request.POST['phone']
        email=request.POST['email']
        seller.seller_name=seller_name
        seller.Address=address
        seller.phone=phone_number
        seller.Email=email
        seller.save()
        log_id.username=seller_name
        log_id.save()
        return HttpResponse("updated!!")
    else:
        return render(request,'Seller/editsellerprofile.html',{'seller':seller})
def view_product(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    product=Product.objects.get(login_id=log_id)
    context={
        'product':product
    }
    return render(request,'Seller/viewproduct.html',context)



def customer_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    context={
        'customer':customer
    }
    return render(request,'Customer/customerprofile.html',context)
def purchase(request):
    return render(request,'Customer/purchase.html')
def edit_customer(request):
    return render(request,'Customer/editprofile.html')


def n_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    context={
        'nutritionist':nutritionist
    }
    return render(request,'Nutritionist/nprofile.html',context)