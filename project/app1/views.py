from django.shortcuts import render,redirect
from .models import Seller,Customer,Hospital,LoginUser,Parent,Nutritionist,Baby_details,Product,Doctor,Cart,Productbooking,Booking,Vaccination,Video,Baby_vaccine
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta

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
        if LoginUser.objects.filter(username=username).exists():
            return render(request,'Home/sreg.html',{'message':"username already exists!!"}) 
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
        if LoginUser.objects.filter(username=username).exists():
            return render(request,'Home/creg.html',{'message':"username already exists!!"})
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
        if LoginUser.objects.filter(username=username).exists():
            return render(request,'Home/hreg.html',{'message':"username already exists!!"})
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
        if LoginUser.objects.filter(username=username).exists():
            return render(request,'Hospital/addparent.html',{'message':"username already exists!!"})
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
        return redirect(view_parent)
    else:
        return render(request,'Hospital/addparent.html')
def search_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    parents=Parent.objects.filter(hospital_id=hospital)
    if request.method=='GET':
        parent_name=request.GET['search']
        parents=Parent.objects.filter(hospital_id=hospital,
                                      parent_name__icontains=parent_name)
        context={
            'parent':parents
            }
        return render(request,'Hospital/viewparents.html',context)
def view_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital_id=Hospital.objects.get(login_id=log_id)
    parents=Parent.objects.filter(hospital_id=hospital_id)
    items_per_page = 5

        # Use Paginator to paginate the products
    paginator = Paginator(parents, items_per_page)
    page = request.GET.get('page', 1)

    try:
        parents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        parents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        parents = paginator.page(paginator.num_pages)
    context={
        'parent': parents
    }
    return render(request,'Hospital/viewparents.html',context)
def delete_parent(request,id):
    parent=Parent.objects.get(id=id)
    parent.delete()
    parents=LoginUser.objects.get(id=parent.login_id.id)
    parents.delete()
    return redirect(view_parent)
def add_baby(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    parent=Parent.objects.get(id=id)
    vaccine=Vaccination.objects.filter(hospital_id=hospital.id,Age=0)
    print(vaccine)
    
    if request.method=='POST':
        baby_name=request.POST['baby_name']
        father_name=request.POST['father_name']
        birth_date=request.POST['birth_date']
        gender=request.POST['gender']
        weight=request.POST['weight']
        blood_group=request.POST['blood_group']
        vaccine=request.POST['vaccine']
        baby_data=Baby_details.objects.create(baby_name=baby_name,
                                              hospital_id=hospital,
                                              
                                              parent_id=parent,
                                              father_name=father_name,
                                              birth_date=birth_date,
                                              gender=gender,
                                              weight=weight,
                                              blood_group=blood_group,)
        baby_data.save()
        vaccine_id=Vaccination.objects.get(id=vaccine)
        baby_id=Baby_details.objects.get(id=baby_data.id)
        baby_vaccine=Baby_vaccine.objects.create(vaccination_id=vaccine_id,
                                                 baby_id=baby_id,
                                                date=birth_date)
        baby_vaccine.save()
        parent.baby_status="True"
        parent.save()
        return redirect(view_parent)
        
        
    else:
        context ={
            'parent':parent,
            'vaccines':vaccine
        }
        return render(request,'Hospital/addbaby.html',context)
def view_baby(request,id):
    parent=Parent.objects.get(id=id)
    baby=Baby_details.objects.filter(parent_id=parent)
    print(baby)
    context={
        'baby':baby
    }

    return render(request,'Hospital/viewbabydetails.html',context)
def add_vaccination(requesst):
    log_id=LoginUser.objects.get(id=requesst.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    if requesst.method=='POST':
        vaccine_name=requesst.POST['Vaccination_name']
        dose=requesst.POST['Dose']
        age=requesst.POST['Age']
        vaccine=Vaccination.objects.create(hospital_id=hospital,
                                           Vaccination_name=vaccine_name,
                                           Dose=dose,
                                           Age=age)
        vaccine.save()
       
        return redirect(mainview_vaccine)
    return render(requesst,'Hospital/addvaccination.html')
def mainview_vaccine(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    vaccine=Vaccination.objects.filter(hospital_id=hospital)
    context={
        'vaccine':vaccine
    }
    return render(request,'Hospital/viewmainvaccine.html',context) 
# def generate_vaccine(request):
#     return render(request,'Hospital/generatevaccine.html') 
def viewbaby_vaccine(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    vaccine=Vaccination.objects.filter(hospital_id=hospital)
    b_id=Baby_details.objects.get(id=id)
    babyvaccine=Baby_vaccine.objects.filter(baby_id=b_id)
    taken_vaccine_ids = babyvaccine.values_list('vaccination_id', flat=True)
    not_taken_vaccines = vaccine.exclude(id__in=taken_vaccine_ids)
    for vaccine in not_taken_vaccines:
        vaccine.age_in_months = vaccine.Age
        vaccine.vaccination_date = b_id.birth_date + timedelta(days=30 * vaccine.age_in_months)
    not_taken_vaccines = sorted(not_taken_vaccines, key=lambda x: x.vaccination_date)
    
    context={
        'vaccines':vaccine,
        'baby':babyvaccine,
        'not_taken_vaccines':not_taken_vaccines,
        'b_id':b_id

    }
    return render(request,'Hospital/babyvaccineview.html',context) 
def date_vtaken(request,id):
    baby=Baby_details.objects.get(id=id)
    if request.method=='POST':
        date=request.POST['date']
        vaccine=request.POST['vaccine_id']
        vaccine_id=Vaccination.objects.get(id=vaccine)
        vdate=Baby_vaccine.objects.create(date=date,
                                          vaccination_id=vaccine_id,
                                          baby_id=baby)
        vdate.save()
        return redirect(viewbaby_vaccine,id=baby.id)
   
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
        if LoginUser.objects.filter(username=username).exists():
            return render(request,'Hospital/addnutritionist.html',{'message':"username already exists!!"})
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
    items_per_page = 5

        # Use Paginator to paginate the products
    paginator = Paginator(doctor, items_per_page)
    page = request.GET.get('page', 1)

    try:
        doctors = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        doctors = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        doctors = paginator.page(paginator.num_pages)
    context={
        'doctor':doctors
    }
    return render(request,'Hospital/viewdoctordetails.html',context)
def search_doctor(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    doctors=Doctor.objects.filter(hospital_id=hospital)
    if request.method=='GET':
        doctor_name=request.GET['search']
        doctors=Doctor.objects.filter(hospital_id=hospital,
                                      Doctor_name__icontains=doctor_name)
        context={
        'doctor':doctors
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


def view_appoinment(request,id):
    doctor=Doctor.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    booking=Booking.objects.filter(doctor_id__hospital_id=hospital,doctor_id=doctor)
    context={
        'booking':booking
    }
    return render(request,'Hospital/viewappoinmentbooking.html',context)
def add_videos(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    
    if request.method=='POST':
        video_title=request.POST['title']
        discription=request.POST['discription']
        videos=request.FILES['video']
        video=Video.objects.create(title=video_title,
                                   hospital_id=hospital,
                                   discription=discription,
                                   video=videos)
        video.save()

        return redirect(view_videos)
    return render(request,'Hospital/addvideos.html')
def view_videos(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    videos=Video.objects.filter(hospital_id=hospital)
    print(videos)
    context={
        'video':videos
    }
    return render(request,'Hospital/viewvideos.html',context)
def edit_videos(request,id):
    video=Video.objects.get(id=id)
    if request.method=='POST':
        video_title=request.POST['title']
        discription=request.POST['discription']
        video.title=video_title
        video.discription=discription
        video.save()
        return redirect(view_videos)
    
    return render(request,'Hospital/editvideos.html',{'video':video})
def delete_videos(request,id):
    video=Video.objects.get(id=id)
    video.delete()
    return redirect(view_videos)




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
def vaccination_chart(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    hospital=parent.hospital_id
    vaccine=Vaccination.objects.filter(hospital_id=hospital)
    b_id=Baby_details.objects.get(id=id)
    babyvaccine=Baby_vaccine.objects.filter(baby_id=b_id)
    taken_vaccine_ids = babyvaccine.values_list('vaccination_id', flat=True)
    not_taken_vaccines = vaccine.exclude(id__in=taken_vaccine_ids)
    for vaccine in not_taken_vaccines:
        vaccine.age_in_months = vaccine.Age
        vaccine.vaccination_date = b_id.birth_date + timedelta(days=30 * vaccine.age_in_months)
    not_taken_vaccines = sorted(not_taken_vaccines, key=lambda x: x.vaccination_date)
    
    context={
        'vaccines':vaccine,
        'baby':babyvaccine,
        'not_taken_vaccines':not_taken_vaccines,
        'b_id':b_id

    }

    return render(request,'Parent/vaccinationchart.html',context)
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
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    hospital= parent.hospital_id
    doctor=Doctor.objects.filter(hospital_id=hospital)
    print(doctor)
    context={
        'doctor':doctor
    }
    
    return render(request,'Parent/doctorslist.html',context)
def parentsearch_doctor(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    hospital=parent.hospital_id
    doctors=Doctor.objects.filter(hospital_id=hospital)
    if request.method=='GET':
        doctor_name=request.GET['search']
        doctors=Doctor.objects.filter(Doctor_name__icontains=doctor_name,
                                hospital_id=hospital)
        context={
            'doctor':doctors

        }
        return render(request,'Parent/doctorslist.html',context)
def doctor_booking(request,id):
    doctor=Doctor.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    

    booking=Booking.objects.create(parent_id=parent,doctor_id=doctor)
    

    booking.save()
    doctor.slots = doctor.slots-1
    doctor.save()
    return redirect(my_appoinments)
def my_appoinments(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    booking=Booking.objects.filter(parent_id=parent)
    context={
        'booking':booking
    }
    return render(request,'Parent/myappoinments.html',context)

def cancel_booking(request,id):
    booking=Booking.objects.get(id=id)
    booking.delete()
    return redirect(my_appoinments)

    
    return render(request,'Parent/doctorbooking.html')
def pview_videos(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    hospital=parent.hospital_id
    videos=Video.objects.filter(hospital_id=hospital)
    context={
        'video':videos
    }
    return render(request,'Parent/pviewvideos.html',context)






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
        return redirect(seller_profile)
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
        image1=request.FILES['image1']
        image2=request.FILES['image2']
        image3=request.FILES['image3']
        product_data=Product.objects.create(seller_id=seller_id,
                                            product_name=product_name,
                                            price=price,
                                            product_details=product_details,
                                            location=location,
                                            image1=image1,
                                            image2=image2,
                                            image3=image3)
        product_data.save()
        return redirect(seller_viewproducts)
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
        if 'image1' in request.FILES:
            product.image1=request.FILES['image1']
        if 'image2' in request.FILES:
            product.image2=request.FILES['image2']
        if 'image3' in request.FILES:
            product.image3=request.FILES['image3']
        product.product_name=product_name
        product.price=price
        product.product_details=product_details
        product.location=location
        product.save()
        return redirect(seller_viewproducts)
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
    log_id=LoginUser.objects.get(id=request.user.id)
    seller=Seller.objects.get(login_id=log_id)
    product=Productbooking.objects.filter(product_id__seller_id=seller)
    print(product)
    context={
        'product':product
    }
    return render(request,'Seller/viewbooking.html',context)
def booking_status(request,id):
    booking=Productbooking.objects.get(id=id)
    if request.method=='POST':
        status=request.POST["status"]
        if status=="approved":
            booking.status=status
        elif status=="rejected":
            booking.status=status
        booking.save()
    return redirect(seller_viewbookings)

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

def edit_customer(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    if request.method=='POST':
        customer_name=request.POST['Customer_name']
        address=request.POST['Address']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        customer.Customer_name=customer_name
        customer.Address=address
        customer.Email=email
        customer.phone=phone_number
        customer.save()
        return redirect(customer_profile)
    else:
        return render(request,'Customer/editprofile.html',{'customer':customer})
def purchase(request):
    product=Product.objects.all()
    context={
        'product':product
    }
    return render(request,'Customer/purchase.html',context)
def product_search(request):
    if request.method=='GET':
        search=request.GET['search']
        products=Product.objects.filter(
            Q(product_name__icontains=search) |
            Q(location__icontains=search))
        context={
            'product':products
        }
        return render(request,'Customer/purchase.html',context)
def add_to_cart(request,id):
    product=Product.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    cart=Cart.objects.create(product_id=product,customer_id=customer)
    cart.save()
    
    return redirect(cart_view)
def cart_view(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    cart=Cart.objects.filter(customer_id=customer)
    print(cart)
    context={
        'cart':cart
    }
    return render(request,'Customer/cart.html',context)
def cart_delete(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect(cart_view)
def cart_booking(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    cart=Cart.objects.filter(customer_id=customer)
    for i in cart:
     cartbooking=Productbooking.objects.create(product_id=i.product_id,
                                                customer_id=i.customer_id,
                                                status='PENDING')
     cartbooking.save()
    cart.delete()

    return redirect(my_orders)
def view_product(request):
    return render(request,'Customer/viewproduct.html')
def product_booking(request,id):
    product=Product.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    booking=Productbooking.objects.create(product_id=product,customer_id=customer)
    booking.save()
    return redirect(my_orders)

def my_orders(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    customer=Customer.objects.get(login_id=log_id)
    product=Productbooking.objects.filter(customer_id=customer)
    context={
        'product':product
    }
    return render(request,'Customer/myorders.html',context)
def payment(request):
    return render(request,'Customer/payment.html')
def view_orders(request):
    return render(request,'Customer/viewmyorder.html')
def delete_order(request,id):
    product=Productbooking.objects.get(id=id)
    product.delete()
    return redirect(my_orders)


def chatlist_seller(request):
    return render(request,'Customer/chatlistseller.html')
def chat_seller(request):
    return render(request,'Customer/chat.html')
 




#nutritionist#

def n_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    context={
        'nutritionist':nutritionist
    }
    return render(request,'Nutritionist/nprofile.html',context)
def nview_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    parents=Parent.objects.filter(hospital_id=nutritionist.hospital_id)
    items_per_page = 5

        # Use Paginator to paginate the products
    paginator = Paginator(parents, items_per_page)
    page = request.GET.get('page', 1)

    try:
        parents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        parents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        parents = paginator.page(paginator.num_pages)
    context={
        'parent': parents
    }
    return render(request,'Nutritionist/viewparentlist.html',context)
def nsearch_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    hospital=Hospital.objects.get(id=nutritionist.hospital_id.id)
    print(hospital)
    if request.method=='GET':
        parent_name=request.GET['search']
        parents=Parent.objects.filter(hospital_id=hospital,
                                      parent_name__icontains=parent_name)
        
        context={
            'parent':parents
            }
        return render(request,'Nutritionist/viewparentlist.html',context)
def parent_msg(request):
    return render(request,'Nutritionist/parentmsg.html')