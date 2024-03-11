from django.shortcuts import render,redirect
from .models import Seller,Customer,Hospital,LoginUser,Parent,Nutritionist,Baby_details,Product,Doctor,Cart
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request,'Home/home.html')
def about(request):
    return render(request,'Home/about.html')
def seller_register(request):
    if request.method=='POST':
        seller_name=request.POST['seller_name']
        address=request.POST['address']
        phone_number=request.POST['phone']
        email=request.POST['email']
        username = request.POST['username']
        password=request.POST['password']    
        password2=request.POST['confirmPassword'] 
        if password != password2:
            return render(request,'Home/sreg.html',{'message':"password doesn't match"})   
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type='seller')
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
        username = request.POST['username']
        password=request.POST['password']
        password1=request.POST['confirmPassword']
        if password != password1:
            return render(request,'Home/creg.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type='customer')
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
        username = request.POST['username']
        password=request.POST['password']
        password2=request.POST['confirmPassword']
        if password != password2:
            return render(request,'Home/hreg.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type="hospital")
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
def loggout(request):  
    logout(request)
    return redirect(loginpage)







#hospital#


def hospital_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    context={
        'hospital':hospital
    }
    return render(request,'Hospital/hospitalprofile.html',context)


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
        # log_id.username=hospital_name
        # log_id.save()
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
        username = request.POST['username']
        password=request.POST['password']
        password2=request.POST['confirmPassword']
        if password != password2:
            return render(request,'Hospital/addparent.html',{'message':"password doesn't match"})
        
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type="parent")
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
        username = request.POST['username']
        password=request.POST['password']
        password1=request.POST['confirmPassword']
        if password != password1:
            return render(request,'Hospital/addnutritionist.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type="nutritionist")
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
def add_doctor_details(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    if request.method=='POST':
        slots=int(request.POST['slots'])
        doctor_name=request.POST['Doctor_name']
        department=request.POST['department']
        qualification=request.POST['qualification']
        consulting_days=request.POST['consulting_days']
        doctor_data=Doctor.objects.create(hospital_id=hospital,
                                          slots=slots,
                                          Doctor_name=doctor_name,
                                          department=department,
                                          qualification=qualification,
                                          consulting_days=consulting_days
                                          )
        doctor_data.save()
        return render(request,'Hospital/adddoctordetails.html',{'message':"successfully added!"})
    else:
        return render(request,'Hospital/adddoctordetails.html')
def view_doctor(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    doctor=Doctor.objects.filter(hospital_id=hospital)
    context={
        'doctor':doctor
    }
    return render(request,'Hospital/viewdoctordetails.html',context)
def edit_doctor(request,id):
    # log_id=LoginUser.objects.get(id=request.user.id)
    # hospital=Hospital.objects.get(login_id=log_id)
    doctor=Doctor.objects.get(id=id)
    if request.method=='POST':
        slots=int(request.POST['slots'])
        doctor_name=request.POST['Doctor_name']
        department=request.POST['department']
        qualification=request.POST['qualification']
        consulting_days=request.POST['consulting_days']
        doctor.slots=slots
        doctor.Doctor_name=doctor_name
        doctor.department=department
        doctor.qualification=qualification
        doctor.consulting_days=consulting_days
        doctor.save()
        return redirect(view_doctor)
    else:
        return render(request,'Hospital/editdoctor.html',{'doctor':doctor})
def delete_doctor(request,id):
    doctor=Doctor.objects.get(id=id)
    doctor.delete()
    return redirect(view_doctor)
def view_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital_id=Hospital.objects.get(login_id=log_id)
    parents=Parent.objects.filter(hospital_id=hospital_id)
    context={
        'parent': parents
    }
    return render(request,'Hospital/viewparents.html',context)
def delete_parent(request,id):
    parent=Parent.objects.get(id=id)
    parent.delete()
    return redirect(view_parent)
def view_appoinment(request):
    return render(request,'Hospital/viewappoinmentbooking.html')

#parent#

def parent_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    context={
        'parent':parent
    }
    return render(request,'Parent/parentprofile.html',context)

def baby_details(request):
     log_id=LoginUser.objects.get(id=request.user.id)
     parent=Parent.objects.get(login_id=log_id)
     baby=Baby_details.objects.filter(parent_id=parent)
     print(baby)
     context={
        'baby':baby
     }

     return render(request,'Parent/babydetails.html',context)
def edit_baby(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    baby=Baby_details.objects.get(parent_id=parent)
    if request.method=='POST':
        baby_name=request.POST['baby_name']
        father_name=request.POST['father_name']
        birth_date=request.POST['birth_date']
        gender=request.POST['gender']
        weight=request.POST['weight']
        blood_group=request.POST['blood_group']
        baby.baby_name=baby_name
        baby.father_name=father_name
        baby.birth_date=birth_date
        baby.gender=gender
        baby.weight=weight
        baby.blood_group=blood_group
        baby.save()
        return HttpResponse("updated!!")
    else:
        return render(request,'Parent/editbabydetails.html',{'baby':baby})
def edit_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    
    if request.method=='POST':
        parent_name=request.POST['parent_name']
        address=request.POST['Address']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        blood_group=request.POST['blood_group']
        parent.parent_name=parent_name
        parent.Address=address
        parent.Email=email
        parent.blood_group=blood_group
        parent.phone=phone_number
        parent.save()
        # log_id.username=parent_name
        # log_id.save()
        return HttpResponse("updated!!")
    else:
        return render(request,'Parent/editparent.html',{'parent':parent})
def doctor_list(request):
    return render(request,'Parent/doctorslist.html')





#seller#

def seller_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    seller=Seller.objects.get(login_id=log_id)
    context={
        'seller':seller
    }
    return render(request,'Seller/sellerprofile.html',context)
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
        # log_id.username=seller_name
        # log_id.save()
        return HttpResponse("updated!!")
    else:
        return render(request,'Seller/editsellerprofile.html',{'seller':seller})
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
def edit_product(request,id):
    # log_id=LoginUser.objects.get(id=request.user.id)
    # seller=Seller.objects.get(login_id=log_id)
    product=Product.objects.get(id=id)
    if request.method=='POST':
        product_name=request.POST['product_name']
        price=request.POST['price']
        product_details=request.POST['product_details']
        location=request.POST['location']
        image=request.FILES['image']
        product.product_name=product_name
        product.price=price
        product.product_details=product_details
        product.location=location
        product.image=image
        product.save()
        return HttpResponse("Updated!")
    else:
        return render(request,'Seller/editproduct.html',{'product':product})
def seller_viewproducts(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    seller=Seller.objects.get(login_id=log_id)
    product=Product.objects.filter(seller_id=seller)
    print(product)
    context={
       'product':product
    }
    
    return render(request,'Seller/sellerviewproduct.html',context)
def delete_product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect(seller_viewproducts)
def seller_viewbookings(request):
    return render(request,'Seller/viewbooking.html')
def chat(request):
    return render(request,'Seller/chat.html')


#customer#

def customer_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    context={
        'customer':customer
    }
    return render(request,'Customer/customerprofile.html',context)
def purchase(request):
    product=Product.objects.all()
    context={
        'product':product
    }
    return render(request,'Customer/purchase.html',context)
def edit_customer(request):
    return render(request,'Customer/editprofile.html')
def view_product(request):
    return render(request,'Customer/viewproduct.html')
def my_orders(request):
    return render(request,'Customer/myorder.html')
def add_to_cart(request,id):
    product=Product.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    cart=Cart.objects.create(product_id=product,customer_id=customer)
    cart.save()
    
    return render(request,'Customer/cart.html')
def cart_view(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    cart=Cart.objects.filter(customer_id=customer)
    print(cart)
    context={
        'cart':cart
    }
    return render(request,'Customer/cart.html',context)
 


#nutritionist#
def n_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    context={
        'nutritionist':nutritionist
    }
    return render(request,'Nutritionist/nprofile.html',context)
