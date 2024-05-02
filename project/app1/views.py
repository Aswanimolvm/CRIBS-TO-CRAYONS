from django.shortcuts import render,redirect
from .models import User,Hospital,LoginUser,Parent,Nutritionist,Baby_details,Product,Doctor,Cart,Productbooking,Booking,Vaccination,Video,Baby_vaccine,Chat,VaccineDocument
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from django.shortcuts import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max 
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField

# Create your views here.
def home(request):
    return render(request,'Home/home.html')
def about(request):
    return render(request,'Home/about.html')
# def seller_register(request):
#     if request.method=='POST':
#         seller_name=request.POST['seller_name']
#         street=request.POST['street']
#         district=request.POST['district']
#         pincode=request.POST['pincode']
#         phone_number=request.POST['phone']
#         email=request.POST['email']
#         username = request.POST['username']
#         password=request.POST['password']    
#         password2=request.POST['confirmPassword']
#         if LoginUser.objects.filter(username=username, user_type='seller').exists():
#             return render(request,'Home/sreg.html',{'message':"username already exists!!"})
#         if Seller.objects.filter(Email=email).exists():
#             return render(request, 'Home/sreg.html', {'message': "Email is already registered!"})

#         # Check if phone number already exists
#         if Seller.objects.filter(phone=phone_number).exists():
#             return render(request, 'Home/sreg.html', {'message': "Phone number is already registered!"}) 
#         if password != password2:
#             return render(request,'Home/sreg.html',{'message':"password doesn't match"})   
#         try:
#             # Create the user
#             login_data = LoginUser.objects.create_user(username=username, password=password, user_type='seller')
#             # Create the seller data
#             seller_data = Seller.objects.create(login_id=login_data, seller_name=seller_name, street=street,district=district,pincode=pincode, Email=email, phone=phone_number)
#             return redirect(loginpage)
#         except Exception:
#             return render(request, 'Home/sreg.html', {'message': "An error occurred while processing your request."})      
#     else:
#         return render(request,'Home/sreg.html')
def user_register(request):
    if request.method=='POST':
        user_name=request.POST['Customer_name']
        street=request.POST['street']
        district=request.POST['district']
        pincode=request.POST['pincode']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        username = request.POST['username']
        password=request.POST['password']
        password1=request.POST['confirmPassword']
        if LoginUser.objects.filter(username=username).exists():
            return render(request,'Home/ureg.html',{'message':"username already exists!!"})
        if User.objects.filter(Email=email).exists():
            return render(request, 'Home/ureg.html', {'message': "Email is already registered!"})

        # Check if phone number already exists
        if User.objects.filter(phone=phone_number).exists():
            return render(request, 'Home/ureg.html', {'message': "Phone number is already registered!"})
        if password != password1:
            return render(request,'Home/ureg.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type='user')
        login_data.save()
        log_id=LoginUser.objects.get(id=login_data.id)
        user_data=User.objects.create(login_id=log_id,user_name=user_name,street=street,district=district,pincode=pincode,Email=email,phone=phone_number)
        user_data.save()
        return redirect(loginpage)
    else:
        return render(request,'Home/ureg.html')

    # return render(request,'Home/creg.html')
def hospital_register(request):
    if request.method=='POST':
        hospital_name=request.POST['hospital_name']
        street=request.POST['street']
        district=request.POST['district']
        pincode=request.POST['pincode']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        licence_proof=request.FILES['licence_proof']
        username = request.POST['username']
        password=request.POST['password']
        password2=request.POST['confirmPassword']
        if LoginUser.objects.filter(username=username,user_type="hospital").exists():
            return render(request,'Home/hreg.html',{'message':"username already exists!!"})
        if Hospital.objects.filter(Email=email).exists():
            return render(request, 'Home/hreg.html', {'message': "Email is already registered!"})

        # Check if phone number already exists
        if Hospital.objects.filter(phone=phone_number).exists():
            return render(request, 'Home/hreg.html', {'message': "Phone number is already registered!"})
        if password != password2:
            return render(request,'Home/hreg.html',{'message':"password doesn't match"})
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type="hospital")
        login_data.save()
        log_id=LoginUser.objects.get(id=login_data.id)
        hospital_data=Hospital.objects.create(login_id=log_id,hospital_name=hospital_name,street=street,district=district,pincode=pincode,Email=email,phone=phone_number,licence_proof=licence_proof)
        hospital_data.save()
        return redirect(loginpage)
    else:
        return render(request,'Home/hreg.html')
    

def loginpage(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
            return redirect(admin_home)
        data=authenticate(username=username,password=password)
        print(data)
        if data is not None:
            login(request,data)
            # if data.user_type=="seller":
            #     return redirect(seller_profile)
            if data.user_type=="user":
                return redirect(purchase)
            elif data.user_type=="hospital" and data.status=="approved":
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

@login_required(login_url='login/')
def hospital_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    context={
        'hospital':hospital
    }
    return render(request,'Hospital/hospitalprofile.html',context)


@login_required(login_url='login/')
def edit_hospital(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    if request.method=='POST':
        hospital_name=request.POST['hospital_name']
        street=request.POST['street']
        district=request.POST['district']
        pincode=request.POST['pincode']
        # email=request.POST['Email']
        # phone_number=request.POST['phone']
        hospital.hospital_name = hospital_name
        hospital.street=street
        hospital.district=district
        hospital.pincode=pincode
        # hospital.Email=email
        # hospital.phone=phone_number
        hospital.save()
        # log_id.username=hospital_name
        # log_id.save()
        return redirect(hospital_profile)
    else:
        return render(request,'Hospital/edithprofile.html',{'hospital':hospital})
    
@login_required(login_url='login/')   
def add_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital_id=Hospital.objects.get(login_id=log_id)
    if request.method=='POST':
        parent_name=request.POST['parent_name']
        street=request.POST['street']
        district=request.POST['district']
        pincode=request.POST['pincode']
        email=request.POST['Email']
        phone_number=request.POST['phone']
        # blood_group=request.POST['blood_group']
        username = request.POST['username']
        password=request.POST['password']
        password2=request.POST['confirmPassword']
        if LoginUser.objects.filter(username=username).exists():
            return render(request,'Hospital/addparent.html',{'message':"username already exists!!"})
        if Parent.objects.filter(Email=email).exists():
            return render(request, 'Hospital/addparent.html', {'message': "Email is already registered!"})

        # Check if phone number already exists
        if Parent.objects.filter(phone=phone_number).exists():
            return render(request, 'Hospital/addparent.html', {'message': "Phone number is already registered!"})
        if password != password2:
            return render(request,'Hospital/addparent.html',{'message':"password doesn't match"})
        
        login_data=LoginUser.objects.create_user(username=username,password=password,user_type="parent")
        login_data.save()
        logg_id=LoginUser.objects.get(id=login_data.id)
        parent_data=Parent.objects.create(
                                        login_id=logg_id,
                                        hospital_id=hospital_id,
                                        parent_name=parent_name,
                                        street=street,
                                        district=district,
                                        pincode=pincode,
                                        Email=email,
                                        phone=phone_number,
                                        )
        parent_data.save()
        return redirect(view_parent)
    else:
        return render(request,'Hospital/addparent.html')
    
@login_required(login_url='login/')    
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
        return render(request,'Hospital/viewparents2.html',context)
    
@login_required(login_url='login/')
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

@login_required(login_url='login/')
def delete_parent(request,id):
    parent=Parent.objects.get(id=id)
    parent.delete()
    parents=LoginUser.objects.get(id=parent.login_id.id)
    parents.delete()
    return redirect(view_parent)

@login_required(login_url='login/')
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
    
@login_required(login_url='login/')
def view_baby(request,id):
    parent=Parent.objects.get(id=id)
    baby=Baby_details.objects.filter(parent_id=parent)
    print(baby)
    context={
        'baby':baby
    }

    return render(request,'Hospital/viewbabydetails.html',context)

@login_required(login_url='login/')
def add_vaccination(requesst):
    log_id=LoginUser.objects.get(id=requesst.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    if requesst.method=='POST':
        vaccine_name=requesst.POST['Vaccination_name']
        dose=requesst.POST['Dose']
        age=requesst.POST['Age']
        days=requesst.POST['days']
        vaccine=Vaccination.objects.create(hospital_id=hospital,
                                           Vaccination_name=vaccine_name,
                                           Dose=dose,
                                           Age=age,
                                           days=days)
        vaccine.save()
       
        return redirect(mainview_vaccine)
    return render(requesst,'Hospital/addvaccination.html')


@login_required(login_url='login/')
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

@login_required(login_url='login/')
def viewbaby_vaccine(request,id):
    b_id = Baby_details.objects.get(id=id)
    # Retrieve parent's ID indirectly through baby's details
    parent_id = b_id.parent_id.id

    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    vaccine=Vaccination.objects.filter(hospital_id=hospital)
    babyvaccine=Baby_vaccine.objects.filter(baby_id=b_id)
    taken_vaccine_ids = babyvaccine.values_list('vaccination_id', flat=True)
    not_taken_vaccines = vaccine.exclude(id__in=taken_vaccine_ids)
    for vaccine in not_taken_vaccines:
        months = vaccine.Age
        days = vaccine.days if vaccine.days else 0
        vaccination_date = b_id.birth_date + timedelta(days=30 * months + days)

        vaccine.age_in_months = months
        vaccine.vaccination_date = vaccination_date

        # Calculate notification date
        notification_date = vaccination_date - timedelta(days=7)

        # if notification_date >= timezone.now().date():
        #     send_notification_to_parent(b_id, vaccine, notification_date)

    not_taken_vaccines = sorted(not_taken_vaccines, key=lambda x: x.vaccination_date)
    # Pass parent_id with each vaccine object in the context
    vaccines_with_parent_id = [{'vaccine': vaccine, 'parent_id': parent_id} for vaccine in not_taken_vaccines]

    for vaccine_data in vaccines_with_parent_id:
        vaccine = vaccine_data['vaccine']
        # Check if the vaccine has any associated requests
        vaccine_data['has_request'] = VaccineDocument.objects.filter(vaccination_id=vaccine.id).exists()


    context={
        'vaccines':vaccine,
        'baby':babyvaccine,
        'not_taken_vaccines':vaccines_with_parent_id,
        'b_id':b_id,

    }
    return render(request,'Hospital/babyvaccineview.html',context)

def view_request(request, id, parent_id):
    # Retrieve the vaccine object
    vaccine = Vaccination.objects.get(id=id)

    # Get update requests related to this vaccine
    update_requests = VaccineDocument.objects.filter(vaccination_id=vaccine, parent_id=parent_id)
    print(update_requests)
    
    # Pass the update requests to the template
    context = {
        'vaccine': vaccine,
        'update_requests': update_requests,
    }
    
    return render(request, 'Hospital/view_request.html', context)

 
def send_notification_to_parent(baby, vaccine, notification_date):
    subject = f"Upcoming Vaccination Reminder for {baby.baby_name}"
    message = f"Dear parent,\n\nThis is a reminder that your child {baby.baby_name} has a vaccination appointment coming up on {vaccine.vaccination_date}. Please ensure that your child is prepared.\n\nSincerely,\nHospital"
    sender = "aswanisubin02@gmail.com"
    recipient = baby.parent_id.Email

    send_mail(subject, message, sender, [recipient]) 

@login_required(login_url='login/')
def date_vtaken(request,id):
    baby=Baby_details.objects.get(id=id)
    if request.method=='POST':
        date=request.POST['date']
        vaccine=request.POST['vaccine_id']
        print(vaccine)
        vaccine_id=Vaccination.objects.get(id=vaccine)
        vdate=Baby_vaccine.objects.create(date=date,
                                          vaccination_id=vaccine_id,
                                          baby_id=baby)
        vdate.save()
        return redirect(viewbaby_vaccine,id=baby.id)

  
def add_nutritionist(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital_id=Hospital.objects.get(login_id=log_id)
    if Nutritionist.objects.filter(hospital_id=hospital_id).exists():
        return render(request, 'Hospital/addnutritionist.html', {'message': "A nutritionist is already added to this hospital."})

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
        nutritionist=Nutritionist.objects.create(login_id=logg_id,
                                                      hospital_id=hospital_id,
                                                      Nutritionist_name=nutritionist_name,
                                                      consulting_days=consulting_days,
                                                      consulting_time=consulting_time
                                                      )
        nutritionist.save()
        return redirect(view_nutritionist)
    else:
         return render(request,'Hospital/addnutritionist.html')
    
@login_required(login_url='login/')
def view_nutritionist(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    nutritionist=Nutritionist.objects.filter(hospital_id=hospital)
    print(nutritionist)
    context={
        'nutritionist':nutritionist
    }
    return render(request,'Hospital/viewnutritionist.html',context)

@login_required(login_url='login/')
def delete_nutritionist(request,id):
    nutritionist=Nutritionist.objects.get(id=id)
    nutritionist.delete()
    return redirect(view_nutritionist)

@login_required(login_url='login/')
def add_doctor_details(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    if request.method=='POST':
        slots=int(request.POST['slots'])
        doctor_name=request.POST['Doctor_name']
        department=request.POST['department']
        qualification=request.POST['qualification']
        consulting_days=request.POST['consulting_days']
        consulting_time=request.POST['consulting_time']
        doctor_data=Doctor.objects.create(hospital_id=hospital,
                                          slots=slots,
                                          Doctor_name=doctor_name,
                                          department=department,
                                          qualification=qualification,
                                          consulting_days=consulting_days,
                                          consulting_time=consulting_time,
                                          )
        doctor_data.save()
        return redirect(view_doctor)
    else:
        return render(request,'Hospital/adddoctordetails.html')
    
@login_required(login_url='login/')
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

@login_required(login_url='login/')
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
        return render(request,'Hospital/viewdoctordetails2.html',context)
    
@login_required(login_url='login/')
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
    
@login_required(login_url='login/')
def delete_doctor(request,id):
    doctor=Doctor.objects.get(id=id)
    doctor.delete()
    return redirect(view_doctor)

@login_required(login_url='login/')
def view_appoinment(request,id):
    doctor=Doctor.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    booking=Booking.objects.filter(doctor_id__hospital_id=hospital,doctor_id=doctor)
    context={
        'booking':booking,
        'doctor' :doctor
    }
    return render(request,'Hospital/viewappoinmentbooking.html',context)

@login_required(login_url='login/')
def hospital_search_appt(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    doctor=Doctor.objects.get(id=id)
    booking=Booking.objects.filter(doctor_id=doctor)
    if request.method=='GET':
        booking_date=request.GET['search']
        booking=Booking.objects.filter(booking_date__icontains=booking_date,
                                doctor_id__hospital_id=hospital,)
        context={
            'booking':booking,
            'doctor':doctor

        }
        return render(request,'Hospital/viewappoinmentbooking.html',context)
    
@login_required(login_url='login/')
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

@login_required(login_url='login/')
def view_videos(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    hospital=Hospital.objects.get(login_id=log_id)
    videos=Video.objects.filter(hospital_id=hospital)
    print(videos)
    context={
        'video':videos
    }
    return render(request,'Hospital/viewvideos.html',context)

@login_required(login_url='login/')
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

@login_required(login_url='login/')
def delete_videos(request,id):
    video=Video.objects.get(id=id)
    video.delete()
    return redirect(view_videos)




#########################################        parent        ###############################################################3#



@login_required(login_url='login/')
def parent_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    context={
        'parent':parent
    }
    return render(request,'Parent/parentprofile.html',context)


@login_required(login_url='login/')
def baby_details(request):
     log_id=LoginUser.objects.get(id=request.user.id)
     parent=Parent.objects.get(login_id=log_id)
     baby=Baby_details.objects.filter(parent_id=parent)
     print(baby)
     context={
        'baby':baby
     }

     return render(request,'Parent/babydetails.html',context)

@login_required(login_url='login/')
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
        return redirect(baby_details)
    else:
        return render(request,'Parent/editbabydetails.html',{'baby':baby})
    
@login_required(login_url='login/')
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
        months = vaccine.Age
        days = vaccine.days if vaccine.days else 0
        vaccination_date = b_id.birth_date + timedelta(days=30 * months + days)

        vaccine.age_in_months = months
        vaccine.vaccination_date = vaccination_date

        # Calculate notification date
        notification_date = vaccination_date - timedelta(days=7)
    not_taken_vaccines = sorted(not_taken_vaccines, key=lambda x: x.vaccination_date)
    
    context={
        'vaccines':vaccine,
        'baby':babyvaccine,
        'not_taken_vaccines':not_taken_vaccines,
        'b_id':b_id

    }

    return render(request,'Parent/vaccinationchart.html',context)



def add_vdocument(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    vaccine_id=Vaccination.objects.get(id=id) 
    if request.method=='POST':
        hospital_name=request.POST['hospital_name']
        document=request.FILES['document']
        vaccine_doc=VaccineDocument.objects.create(parent_id=parent,vaccination_id=vaccine_id,hospital_name=hospital_name,document=document)
        vaccine_doc.save()
        return redirect(view_vdocument, vaccine_id.id)
    else:
        return render(request,'Parent/updationrequest.html',{'vaccine':vaccine_id})
    

@login_required(login_url='login/')
def view_vdocument(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    vaccine=Vaccination.objects.get(id=id)
    vaccinedoc=VaccineDocument.objects.filter(parent_id=parent,vaccination_id=vaccine)
    context={
        'vaccinedoc':vaccinedoc
    }
    return render(request,'Parent/viewdoc.html',context)



@login_required(login_url='login/')
def edit_parent(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    
    if request.method=='POST':
        parent_name=request.POST['parent_name']
        street=request.POST['street']
        district=request.POST['district']
        pincode=request.POST['pincode']
        # email=request.POST['Email']
        # phone_number=request.POST['phone']
        # blood_group=request.POST['blood_group']
        parent.parent_name=parent_name
        parent.street=street
        parent.district=district
        parent.pincode=pincode
        # parent.Email=email
        # parent.phone=phone_number
        parent.save()
        # log_id.username=parent_name
        # log_id.save()
        return redirect(parent_profile)
    else:
        return render(request,'Parent/editparent.html',{'parent':parent})
    
@login_required(login_url='login/')
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

@login_required(login_url='login/')
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
    

@login_required(login_url='login/')
def doctor_booking(request,id):
    doctor=Doctor.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)

    if request.method == "POST": 
        date = request.POST['consulting_date']

        # Check if the user has already booked the doctor for the selected day
        existing_booking = Booking.objects.filter(doctor_id=doctor, parent_id=parent, booking_date=date).exists()
        if existing_booking:
            hospital= parent.hospital_id
            doctor=Doctor.objects.filter(hospital_id=hospital)
            print(doctor)
            context={
            'doctor':doctor,
            'message':"You have already booked this doctor for the selected day."
            }
            return render(request,'Parent/doctorslist.html',context)

        today_bookings_count = Booking.objects.filter(doctor_id=doctor, booking_date=date).count()
        print(today_bookings_count)
        if today_bookings_count >= doctor.slots:
            hospital= parent.hospital_id
            doctor=Doctor.objects.filter(hospital_id=hospital)
            print(doctor)
            context={
            'doctor':doctor,
            'message':"No available slots for today."
            }
            return render(request,'Parent/doctorslist.html',context)

        

        # Generate token for the booking
        booking_date = datetime.now().date()
        token_number = Booking.get_next_token(doctor_id=doctor,parent_id=parent, booking_date=date)
        print(booking_date)
        print(token_number)

        # Calculate start and end times for the booking
        consulting_time = doctor.consulting_time
        start_time = datetime.combine(datetime.now().date(), consulting_time) + timedelta(minutes=30 * (token_number - 1))
        end_time = start_time + timedelta(minutes=30 * (token_number - 1))
        end_time_plus_30min = start_time + timedelta(minutes=30 * token_number)
        booking = Booking.objects.create(
            doctor_id=doctor,
            parent_id=parent,
            booking_date=date,
            token_number=token_number,
            start_time=start_time.time(),
            end_time=end_time_plus_30min.time()
        )

        # Update doctor's available slots
        # doctor.slots -= 1
        # doctor.save()
        return redirect(my_appoinments)


@login_required(login_url='login/')
def my_appoinments(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    bookings=Booking.objects.filter(parent_id=parent)
    context={
        'booking':bookings
    }
     
    return render(request,'Parent/myappoinments.html',context)


@login_required(login_url='login/')
def cancel_booking(request,id):
    booking=Booking.objects.get(id=id)
    doctor=Doctor.objects.get(id=booking.doctor_id.id)
    booking.delete()
    
    return redirect(my_appoinments)

    
    return render(request,'Parent/doctorbooking.html')

@login_required(login_url='login/')
def pview_videos(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    hospital=parent.hospital_id
    videos=Video.objects.filter(hospital_id=hospital)
    context={
        'video':videos
    }
    return render(request,'Parent/pviewvideos.html',context)

@login_required(login_url='login/')
def chat_nutritionist(request):
    sender=request.user
    parent=Parent.objects.get(login_id=sender)
    hospital=parent.hospital_id
    nutritionist=Nutritionist.objects.get(hospital_id=hospital)
    receiver=nutritionist.login_id
    messages = Chat.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).order_by('timestamp')
    return render(request, 'Parent/chat.html', {'sender': sender, 'receiver': receiver, 'messages': messages})

@login_required(login_url='login/')
def purchaseee(request):
    available_products = Product.objects.exclude(
        id__in=Productbooking.objects.filter(status__in=['paid', 'booked']).values('product_id')
    )
    print(available_products)
    context={
        'product':available_products
    }
    return render(request,'Parent/purchase.html',context)

@login_required(login_url='login/')
def product__search(request):
    if request.method=='GET':
        search=request.GET['search']
        products=Product.objects.filter(
            Q(product_name__icontains=search) |
            Q(location__icontains=search))
        context={
            'product':products
        }
        return render(request,'Parent/purchase.html',context)
    

@login_required(login_url='login/')
def add__tocart(request,id):
    product=Product.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    cart_exists = Cart.objects.filter(product_id=product, parent_id=parent).exists()
    if cart_exists:
        return redirect(cart___view)
    else:
        cart=Cart.objects.create(product_id=product,parent_id=parent)
        cart.save()
        return redirect(cart___view)
    
@login_required(login_url='login/')
def cart___view(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    cart=Cart.objects.filter(parent_id=parent)
    print(cart)
    context={
        'cart':cart
    }
    return render(request,'Parent/cart.html',context)


@login_required(login_url='login/')
def cart__delete(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect(cart___view)

@login_required(login_url='login/')
def cart__booking(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    cart=Cart.objects.filter(parent_id=parent)
    
    for i in cart:
     if Productbooking.objects.filter(product_id=i.product_id).exists():
        return redirect(my__orders)
     cartbooking=Productbooking.objects.create(product_id=i.product_id,
                                                parent_id=i.parent_id,
                                                status='pending')
     
     cartbooking.save()
    cart.delete()

    return redirect(my__orders)

# @login_required(login_url='login/')
# def view_product(request):
#     return render(request,'Customer/viewproduct.html')

@login_required(login_url='login/')
def product__booking(request,id):
    product=Product.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    canceled_booking = Productbooking.objects.filter(product_id=product, status='cancelled').first()
    if canceled_booking:
        # If a canceled booking exists, update its status to 'pending' and assign the current parent
        canceled_booking.status = 'pending'
        canceled_booking.parent_id = parent
        canceled_booking.save()
        return redirect(my__orders)
    else:
        # If no canceled booking exists, create a new booking
        booking = Productbooking.objects.create(product_id=product, parent_id=parent)
        booking.save()
        return redirect(my__orders)


@login_required(login_url='login/')
def my__orders(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    parent=Parent.objects.get(login_id=log_id)
    sorting_conditions = Case(
        When(status='booked', then=Value(1)),
        When(status='approved', then=Value(2)),
        When(status='rejected', then=Value(3)),
        default=Value(0),  # Assign a high value for any other status
        output_field=IntegerField(),
    )

    # Fetch bookings for products associated with the seller and order them using custom sorting conditions
    # product = Productbooking.objects.filter(product_id__seller_id=seller).order_by(sorting_conditions)
    product=Productbooking.objects.filter(parent_id=parent).order_by(sorting_conditions)
    context={
        'product':product
    }
    return render(request,'Parent/myorders.html',context)


@login_required(login_url='login/')
def delete__order(request,id):
    product=Productbooking.objects.get(id=id)
    product.status="cancelled"
    product.save()
    return redirect(my__orders)


@login_required(login_url='login/')
def paymentt(request,id):
    booking=Productbooking.objects.get(id=id)
    context={
        'booking':booking
    }
    return render(request,'Parent/payment.html',context)

@login_required(login_url='login/')
def confirm__payment(request,id):
    booking=Productbooking.objects.get(id=id)
    booking.status="paid"
    booking.save()
    return redirect(my__orders)

@login_required(login_url='login/')
def cash__on__delivery(request,id):
    booking=Productbooking.objects.get(id=id)
    booking.status="cash on delivery"
    booking.save()
    return redirect(my__orders)


@login_required(login_url='login/')
def chat__seller(request, product_id):
    sender=request.user
    product=Product.objects.get(id=product_id)
    seller=User.objects.get(id=product.user_id_id)
    receiver=seller.login_id
    print(sender.id)
    print(receiver.id)
    messages = Chat.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).order_by('timestamp')
    return render(request, 'Parent/chatseller.html', {'sender': sender, 'receiver': receiver, 'messages': messages})







############################################        seller          ##############################################################


# @login_required(login_url='login/')
# def seller_profile(request):
#     log_id=LoginUser.objects.get(id=request.user.id)
#     seller=Seller.objects.get(login_id=log_id)
#     context={
#         'seller':seller
#     }
#     return render(request,'Seller/sellerprofile.html',context)

# @login_required(login_url='login/')
# def edit_seller(request):
#     log_id=LoginUser.objects.get(id=request.user.id)
#     seller=Seller.objects.get(login_id=log_id)
#     if request.method=='POST':
#         seller_name=request.POST['seller_name']
#         street=request.POST['street']
#         district=request.POST['district']
#         pincode=request.POST['pincode']
#         # phone_number=request.POST['phone']
#         # email=request.POST['email']
#         seller.seller_name=seller_name
#         seller.street=street
#         seller.district=district
#         seller.pincode=pincode
#         # seller.phone=phone_number
#         # seller.Email=email
#         seller.save()
#         # log_id.username=seller_name
#         # log_id.save()
#         return redirect(seller_profile)
#     else:
#         return render(request,'Seller/editsellerprofile.html',{'seller':seller})
    
# @login_required(login_url='login/')
# def add_product(request):
#     log_id=LoginUser.objects.get(id=request.user.id)
#     seller_id=Seller.objects.get(login_id=log_id)
#     if request.method=='POST':
#         product_name=request.POST['product_name']
#         price=request.POST['price']
#         product_details=request.POST['product_details']
#         location=request.POST['location']
#         image1=request.FILES['image1']
#         image2=request.FILES['image2']
#         image3=request.FILES['image3']
#         product_data=Product.objects.create(seller_id=seller_id,
#                                             product_name=product_name,
#                                             price=price,
#                                             product_details=product_details,
#                                             location=location,
#                                             image1=image1,
#                                             image2=image2,
#                                             image3=image3)
#         product_data.save()
#         return redirect(seller_viewproducts)
#     return render(request,'Seller/addproducts.html')

# @login_required(login_url='login/')
# def edit_product(request,id):
#     # log_id=LoginUser.objects.get(id=request.user.id)
#     # seller=Seller.objects.get(login_id=log_id)
#     product=Product.objects.get(id=id)
#     if request.method=='POST':
#         product_name=request.POST['product_name']
#         price=request.POST['price']
#         product_details=request.POST['product_details']
#         location=request.POST['location']
#         if 'image1' in request.FILES:
#             product.image1=request.FILES['image1']
#         if 'image2' in request.FILES:
#             product.image2=request.FILES['image2']
#         if 'image3' in request.FILES:
#             product.image3=request.FILES['image3']
#         product.product_name=product_name
#         product.price=price
#         product.product_details=product_details
#         product.location=location
#         product.save()
#         return redirect(seller_viewproducts)
#     else:
#         return render(request,'Seller/editproduct.html',{'product':product})
    
# @login_required(login_url='login/')
# def seller_viewproducts(request):
#     log_id=LoginUser.objects.get(id=request.user.id)
#     seller=Seller.objects.get(login_id=log_id)
#     product=Product.objects.filter(seller_id=seller)
#     print(product)
#     context={
#        'product':product
#     }
    
#     return render(request,'Seller/sellerviewproduct.html',context)

# @login_required(login_url='login/')
# def delete_product(request,id):
#     product=Product.objects.get(id=id)
#     product.delete()
#     return redirect(seller_viewproducts)

# @login_required(login_url='login/')
# def seller_viewbookings(request):
#     log_id=LoginUser.objects.get(id=request.user.id)
#     seller=Seller.objects.get(login_id=log_id)
#     sorting_conditions = Case(
#         When(status='booked', then=Value(1)),
#         When(status='approved', then=Value(2)),
#         When(status='rejected', then=Value(3)),
#         default=Value(0),  # Assign a high value for any other status
#         output_field=IntegerField(),
#     )

#     # Fetch bookings for products associated with the seller and order them using custom sorting conditions
#     product = Productbooking.objects.filter(product_id__seller_id=seller).order_by(sorting_conditions)
#     print(product)
#     context={
#         'product':product
#     }
#     return render(request,'Seller/viewbooking.html',context)

# @login_required(login_url='login/')
# def booking_status(request,id):
#     booking=Productbooking.objects.get(id=id)
#     if request.method=='POST':
#         status=request.POST["status"]
#         if status=="approved":
#             booking.status=status
#             booking.save()
#             Productbooking.objects.filter(product_id=booking.product_id).exclude(status='approved').delete()
#             return redirect(seller_viewbookings)
#         elif status=="rejected":
#             booking.status=status
#             booking.save()
#             return redirect(seller_viewbookings)
        
# @login_required(login_url='login/')
# def confirm(request,id):
#     booking=Productbooking.objects.get(id=id)
#     booking.status="paid"
#     booking.save()
#     return redirect(seller_viewbookings)


# @login_required(login_url='login/')
# def chat(request,id):
#     seller = LoginUser.objects.get(id=request.user.id)
#     productbooking = Productbooking.objects.get(id=id)
#     customer_id = Customer.objects.get(id=productbooking.customer_id.id)
#     customer = customer_id.login_id
#     messages = Chat.objects.filter(Q(sender=seller.id, receiver=customer) | Q(sender=customer, receiver=seller.id)).order_by('timestamp')
#     return render(request, 'Seller/chat.html', {'sender': seller, 'receiver': customer, 'messages': messages})


# @login_required(login_url='login/')
# def chatt(request,id):
#     seller = LoginUser.objects.get(id=request.user.id)
#     productbooking = Productbooking.objects.get(id=id)
#     parent_id = Parent.objects.get(id=productbooking.parent_id.id)
#     parent = parent_id.login_id
#     messages = Chat.objects.filter(Q(sender=seller.id, receiver=parent) | Q(sender=parent, receiver=seller.id)).order_by('timestamp')
#     return render(request, 'Seller/chat.html', {'sender': seller, 'receiver': parent, 'messages': messages})


#########################################           customer             ############################################################


@login_required(login_url='login/')
def user_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    context={
        'user':user
    }
    return render(request,'Customer/customerprofile.html',context)

@login_required(login_url='login/')
def chat_seller(request, product_id):
    sender=request.user
    product=Product.objects.get(id=product_id)
    user=User.objects.get(id=product.user_id.id)
    receiver=user.login_id
    print(sender.id)
    print(receiver.id)
    messages = Chat.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).order_by('timestamp')
    return render(request, 'Customer/chat.html', {'sender': sender, 'receiver': receiver, 'messages': messages})



@login_required(login_url='login/')
def chat(request,id):
    seller = LoginUser.objects.get(id=request.user.id)
    productbooking = Productbooking.objects.get(id=id)
    customer_id = User.objects.get(id=productbooking.user_id.id)
    customer = customer_id.login_id
    messages = Chat.objects.filter(Q(sender=seller.id, receiver=customer) | Q(sender=customer, receiver=seller.id)).order_by('timestamp')
    return render(request, 'Customer/chattt.html', {'sender': seller, 'receiver': customer, 'messages': messages})


@login_required(login_url='login/')
def chat_parent(request,id):
    seller = LoginUser.objects.get(id=request.user.id)
    productbooking = Productbooking.objects.get(id=id)
    parent_id = Parent.objects.get(id=productbooking.parent_id.id)
    parent = parent_id.login_id
    messages = Chat.objects.filter(Q(sender=seller.id, receiver=parent) | Q(sender=parent, receiver=seller.id)).order_by('timestamp')
    return render(request, 'Customer/pchat.html', {'sender': seller, 'receiver': parent, 'messages': messages})

@csrf_exempt
def send_message(request, sender_id, receiver_id):
    if request.method == 'POST':
        sender = LoginUser.objects.get(id=sender_id)
        receiver = LoginUser.objects.get(id=receiver_id)
        print(sender)
        print(receiver)
        message = request.POST.get('message', '')
        print(message)
        if message.strip() != '':
            # Create the new message
            new_message = Chat.objects.create(sender=sender, receiver=receiver, message=message)
            # Prepare the data to send back as JSON response
            response_data = {
                'status': 'ok',
                'message': {
                    'sender': sender.username,
                    'message': message
                }
            }
            return JsonResponse(response_data)
    # Return an error if the request method is not POST or the message is empty
    return JsonResponse({'status': 'error'})

@login_required(login_url='login/')
def edit_customer(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    if request.method=='POST':
        user_name=request.POST['user_name']
        street=request.POST['street']
        district=request.POST['district']
        pincode=request.POST['pincode']
        # email=request.POST['Email']
        # phone_number=request.POST['phone']
        user.user_name=user_name
        user.street=street
        user.district=district
        user.pincode=pincode
        # customer.Email=email
        # customer.phone=phone_number
        user.save()
        return redirect(user_profile)
    else:
        return render(request,'Customer/editprofile.html',{'user':user})
    



@login_required(login_url='login/')
def add__product(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user_id=User.objects.get(login_id=log_id)
    if request.method=='POST':
        product_name=request.POST['product_name']
        price=request.POST['price']
        product_details=request.POST['product_details']
        location=request.POST['location']
        image1=request.FILES['image1']
        image2=request.FILES['image2']
        image3=request.FILES['image3']
        product_data=Product.objects.create(user_id=user_id,
                                            product_name=product_name,
                                            price=price,
                                            product_details=product_details,
                                            location=location,
                                            image1=image1,
                                            image2=image2,
                                            image3=image3)
        product_data.save()
        return redirect(seller__viewproducts)
    else:
        return render(request,'Customer/addproduct.html')

@login_required(login_url='login/')
def edit__product(request,id):
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
        return redirect(seller__viewproducts)
    else:
        return render(request,'Customer/editproduct.html',{'product':product})
    
@login_required(login_url='login/')
def seller__viewproducts(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    product=Product.objects.filter(user_id=user)
    print(product)
    context={
       'product':product
    }
    
    return render(request,'Customer/sellerviewproduct.html',context)

@login_required(login_url='login/')
def delete__product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect(seller__viewproducts)


@login_required(login_url='login/')
def seller__viewbookings(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    sorting_conditions = Case(
        When(status='booked', then=Value(1)),
        When(status='approved', then=Value(2)),
        When(status='rejected', then=Value(3)),
        default=Value(0),  # Assign a high value for any other status
        output_field=IntegerField(),
    )

    # Fetch bookings for products associated with the seller and order them using custom sorting conditions
    product = Productbooking.objects.filter(product_id__user_id=user).order_by(sorting_conditions)
    print(product)
    context={
        'product':product
    }
    return render(request,'Customer/viewbooking.html',context)

@login_required(login_url='login/')
def booking__status(request,id):
    booking=Productbooking.objects.get(id=id)
    if request.method=='POST':
        status=request.POST["status"]
        if status=="approved":
            booking.status=status
            booking.save()
            Productbooking.objects.filter(product_id=booking.product_id).exclude(status='approved').delete()
            return redirect(seller__viewbookings)
        elif status=="rejected":
            booking.status=status
            booking.save()
            return redirect(seller__viewbookings)
        
@login_required(login_url='login/')
def confirmm(request,id):
    booking=Productbooking.objects.get(id=id)
    booking.status="paid"
    booking.save()
    return redirect(seller__viewbookings)



    
@login_required(login_url='login/')
def purchase(request):
    available_products = Product.objects.exclude(
        id__in=Productbooking.objects.filter(status__in=['paid', 'booked']).values('product_id')
    )

    context={
        'product':available_products
    }
    return render(request,'Customer/purchase.html',context)

@login_required(login_url='login/')
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
    
@login_required(login_url='login/')
def add_to_cart(request,id):
    product=Product.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    cart_exists = Cart.objects.filter(product_id=product, user_id=user).exists()
    if cart_exists:
        return redirect(cart_view)
    else:
        cart=Cart.objects.create(product_id=product,user_id=user)
        cart.save()
        return redirect(cart_view)
    
@login_required(login_url='login/')
def cart_view(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    cart=Cart.objects.filter(user_id=user)
    print(cart)
    context={
        'cart':cart
    }
    return render(request,'Customer/cart.html',context)

@login_required(login_url='login/')
def cart_delete(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    return redirect(cart_view)

@login_required(login_url='login/')
def cart_booking(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    cart=Cart.objects.filter(user_id=user)
    
    for i in cart:
     if Productbooking.objects.filter(product_id=i.product_id).exists():
        return redirect(my_orders)
     cartbooking=Productbooking.objects.create(product_id=i.product_id,
                                                user_id=i.user_id,
                                                status='pending')
     
     cartbooking.save()
    cart.delete()

    return redirect(my_orders)

@login_required(login_url='login/')
def view_product(request):
    return render(request,'Customer/viewproduct.html')

@login_required(login_url='login/')
def product_booking(request,id):
    product=Product.objects.get(id=id)
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    if Productbooking.objects.filter(product_id=product,user_id=user,status__in=['approved', 'rejected','cancelled','pending']).exists():
        return redirect(my_orders)
    booking=Productbooking.objects.create(product_id=product,user_id=user)
    booking.save()
    return redirect(my_orders)


@login_required(login_url='login/')
def my_orders(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    user=User.objects.get(login_id=log_id)
    print(user)
    sorting_conditions = Case(
        When(status='booked', then=Value(1)),
        When(status='approved', then=Value(2)),
        When(status='rejected', then=Value(3)),
        default=Value(0),  # Assign a high value for any other status
        output_field=IntegerField(),
    )

    # Fetch bookings for products associated with the seller and order them using custom sorting conditions
    # product = Productbooking.objects.filter(product_id__seller_id=seller).order_by(sorting_conditions)
    product=Productbooking.objects.filter(user_id=user).order_by(sorting_conditions)
    print(product)
    context={
        'product':product
    }
    return render(request,'Customer/myorders.html',context)

@login_required(login_url='login/')
def payment(request,id):
    booking=Productbooking.objects.get(id=id)
    context={
        'booking':booking
    }
    return render(request,'Customer/payment.html',context)

@login_required(login_url='login/')
def confirm_payment(request,id):
    booking=Productbooking.objects.get(id=id)
    booking.status="paid"
    booking.save()
    return redirect(my_orders)

@login_required(login_url='login/')
def cash_on_delivery(request,id):
    booking=Productbooking.objects.get(id=id)
    booking.status="cash on delivery"
    booking.save()
    return redirect(my_orders)

@login_required(login_url='login/')
def view_orders(request):
    return render(request,'Customer/viewmyorder.html')

@login_required(login_url='login/')
def delete_order(request,id):
    product=Productbooking.objects.get(id=id)
    product.status="cancelled"
    product.save()
    return redirect(my_orders)




#################################    ADMIN     ########################################


@login_required(login_url='login/')
def admin_home(request):
    return render(request,'admin/adminhome.html')

@login_required(login_url='login/')
def admin_customer(request):
    customer_data=User.objects.all()
    context={
        'user':customer_data
    }
    return render(request,'admin/customerview.html',context)


@login_required(login_url='login/')
def hospital_view(request):
    hospital_data=Hospital.objects.all()
    items_per_page = 5

        # Use Paginator to paginate the products
    paginator = Paginator(hospital_data, items_per_page)
    page = request.GET.get('page', 1)

    try:
        hospital_data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        hospital_data = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        hospital_data = paginator.page(paginator.num_pages)
   
    context={
        'hospital':hospital_data
    }
    return render(request,'admin/hospitalview.html',context)


@login_required(login_url='login/')
def hospital_search(request):
    if request.method=='GET':
        search=request.GET['search']
        hospital=Hospital.objects.filter(
            Q(hospital_name__icontains=search))
        context={
            'hospital':hospital
        }
        return render(request,'admin/hospitalview.html',context)
    
@login_required(login_url='login/')
def admin_approval(request,id):
    hospital=LoginUser.objects.get(id=id)
    print(hospital)
    if request.method=='POST':
        status=request.POST["status"]
        if status=="approved":
            hospital.status=status
            hospital.save()
            return redirect(hospital_view)
        elif status=="rejected":
            hospital.status=status
            hospital.save()
            return redirect(hospital_view)


@login_required(login_url='login/')
def admin_seller(request):
    seller_data=Seller.objects.all()
    context={
        'seller':seller_data
    }
    return render(request,'admin/sellerview.html',context)




 




#nutritionist#


@login_required(login_url='login/')
def n_profile(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    context={
        'nutritionist':nutritionist
    }
    return render(request,'Nutritionist/nprofile.html',context)

@login_required(login_url='login/')
def edit_nutritionist(request):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    if request.method=='POST':
        nutritionist_name=request.POST['Nutritionist_name']
        consulting_days=request.POST['consulting_days']
        consulting_time=request.POST['consulting_time']
        nutritionist.Nutritionist_name=nutritionist_name
        nutritionist.consulting_days=consulting_days
        nutritionist.consulting_time=consulting_time
        nutritionist.save()
        return redirect(n_profile)
    else:
        return render(request,'Nutritionist/neditprofile.html',{'nutritionist':nutritionist})

@login_required(login_url='login/')   
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

@login_required(login_url='login/')
def nview_baby(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    hospital= nutritionist.hospital_id
    parent=Parent.objects.get(id=id)
    baby=Baby_details.objects.filter(hospital_id=hospital,parent_id=parent)
    context={
        'baby':baby
    }
    return render(request,'Nutritionist/viewbaby.html',context)

@login_required(login_url='login/')
def nbaby_vaccine(request,id):
    log_id=LoginUser.objects.get(id=request.user.id)
    nutritionist=Nutritionist.objects.get(login_id=log_id)
    hospital=Hospital.objects.get(id=nutritionist.hospital_id.id)
    baby=Baby_details.objects.get(id=id)
    babyvaccine=Baby_vaccine.objects.filter(baby_id=baby)
    vaccine=Vaccination.objects.filter(hospital_id=hospital)

    taken_vaccine_ids = babyvaccine.values_list('vaccination_id', flat=True)
    print(taken_vaccine_ids)
    not_taken_vaccines = vaccine.exclude(id__in=taken_vaccine_ids)
    for vaccine in not_taken_vaccines:
        vaccine.age_in_months = vaccine.Age
        vaccine.vaccination_date = baby.birth_date + timedelta(days=30 * vaccine.age_in_months)
    not_taken_vaccines = sorted(not_taken_vaccines, key=lambda x: x.vaccination_date)
    
    context={
        'vaccines':vaccine,
        'baby':babyvaccine,
        'not_taken_vaccines':not_taken_vaccines,
        'b_id':baby

    }
    return render(request,'Nutritionist/babyvaccine.html',context)

@login_required(login_url='login/')
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
        return render(request,'Nutritionist/parentlist2.html',context)
    
@login_required(login_url='login/')
def parent_msg(request,id):
    sender=request.user
    parent=Parent.objects.get(login_id=id)
    receiver=parent.login_id
    print(receiver)
    messages = Chat.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)).order_by('timestamp')
    return render(request, 'Nutritionist/chat.html', {'sender': sender, 'receiver': receiver, 'messages': messages})

@login_required(login_url='login/')
def chat_list(request):
    # Retrieve conversations where the current user is the receiver
    conversations = Chat.objects.filter(receiver=request.user)

    # Group conversations by sender and get the latest message timestamp for each sender
    grouped_conversations = conversations.values('sender').annotate(
        latest_message_time=Max('timestamp')
    ).order_by('-latest_message_time')

    # Retrieve complete chat objects based on the latest message timestamp
    sorted_conversations = []
    for conversation in grouped_conversations:
        sender_id = conversation['sender']
        latest_message_time = conversation['latest_message_time']
        latest_message = Chat.objects.filter(sender_id=sender_id, receiver=request.user, timestamp=latest_message_time).first()
        sorted_conversations.append(latest_message)

    return render(request, 'Nutritionist/parentmsg.html', {'conversations': sorted_conversations})

@login_required(login_url='login/')
def msg(request):
    return render(request,'Customer/chatlistseller.html')

@login_required(login_url='login/')
def list(request):
     # Retrieve conversations where the current user is the receiver
    conversations = Chat.objects.filter(receiver=request.user)

    # Group conversations by sender and get the latest message timestamp for each sender
    grouped_conversations = conversations.values('sender').annotate(
        latest_message_time=Max('timestamp')
    ).order_by('-latest_message_time')

    # Retrieve complete chat objects based on the latest message timestamp
    sorted_conversations = []
    for conversation in grouped_conversations:
        sender_id = conversation['sender']
        latest_message_time = conversation['latest_message_time']
        latest_message = Chat.objects.filter(sender_id=sender_id, receiver=request.user, timestamp=latest_message_time).first()
        sorted_conversations.append(latest_message)

    return render(request,'Nutritionist/list.html',{'conversations': sorted_conversations})
   