"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #home#
    path('',views.home,name="home"),
    path('sellerreg',views.seller_register,name="sellerreg"),
    path('customerreg',views.customer_register,name="customerreg"),
    path('hospitalreg',views.hospital_register,name="hospitalreg"),
    path('login',views.loginpage,name="login"),
    path('logout',views.loggout,name="logout"),
    path('about',views.about,name="about"),

    #seller#
    path('sellerprofile',views.seller_profile,name="sellerprofile"),
    path('editseller',views.edit_seller,name="editseller"),
    path('addproduct',views.add_product,name="addproduct"),
    path('editproduct/<int:id>',views.edit_product,name="editproduct"),
    path('sellerviewproduct',views.seller_viewproducts,name="sellerviewproduct"),
    path('sellerviewbooking',views.seller_viewbookings,name="sellerviewbooking"),
    path('bookingstatus/<int:id>',views.booking_status,name="bookingstatus"),
    path('chat',views.chat,name="chat"),
    path('deleteproduct/<int:id>',views.delete_product,name="deleteproduct"),
    

    #customer#
    path('customerprofile',views.customer_profile,name="customerprofile"),
    path('edicustomer',views.edit_customer,name="edicustomer"),
    path('purchase',views.purchase,name="purchase"),
    path('cart',views.cart_view,name="cart"),
    path('viewproduct',views.view_product,name="viewproduct"),
    path('productbooking/<int:id>',views.product_booking,name="productbooking"),
    path('myorders',views.my_orders,name="myorders"),
    path('vieworders',views.view_orders,name="vieworders"),
    path('addtocart/<int:id>',views.add_to_cart,name="addtocart"),
    path('chatwithseller',views.chat_withseller,name="chatwithseller"),

    #hospital#
    path('hospitalprofile',views.hospital_profile,name="hospitalprofile"),
    path('edithospital',views.edit_hospital,name="edithospital"),
    path('addparent',views.add_parent,name="addparent"),
    path('addbaby/<int:id>',views.add_baby,name="addbaby"),
    path('addnutritionist',views.add_nutritionist,name="addnutritionist"),
    path('adddoctordetails',views.add_doctor_details,name="adddoctordetails"),
    path('viewparents',views.view_parent,name="viewparents"),
    path('editdoctordetails/<int:id>',views.edit_doctor,name="editdoctordetails"),
    path('viewbabyh/<int:id>',views.view_baby,name="viewbabyh"),
    path('viewdoctorlist',views.view_doctor,name="viewdoctorlist"),
    path('deletedoctor/<int:id>',views.delete_doctor,name="deletedoctor"),
    path('deleteparent/<int:id>',views.delete_parent,name="deleteparent"),
    path('viewappoinment',views.view_appoinment,name="viewappoinment"),
    path('addvideos',views.add_videos,name="addvideos"),
    path('viewvideos',views.view_videos,name="viewvideos"),
    path('parentviewvideos',views.pview_videos,name="parentviewvideos"),
    path('editvideos',views.edit_videos,name="editvideos"),

    #nutritionist#
    path('nprofile',views.n_profile,name="nprofile"),
    path('viewparentlist',views.view_parentlist,name="viewparentlist"),
    path('parentmsg',views.parent_msg,name="parentmsg"),

    #parent#
    path('parentprofile',views.parent_profile,name="parentprofile"),
    path('babydetails',views.baby_details,name="babydetails"),
    path('editbabydetails',views.edit_baby,name="editbabydetails"),
    path('editparentprofile',views.edit_parent,name="editparentprofile"),
    path('doctorlist',views.doctor_list,name="doctorlist"),
    path('doctorbooking',views.doctor_booking,name="doctorbooking"),
    
   
    
    
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
