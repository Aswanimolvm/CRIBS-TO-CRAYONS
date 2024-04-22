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
    
    #home#
    path('',views.home,name="home"),
    path('sellerreg',views.seller_register,name="sellerreg"),
    path('customerreg',views.customer_register,name="customerreg"),
    path('hospitalreg',views.hospital_register,name="hospitalreg"),
    path('login/',views.loginpage,name="login"),
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
    path('confirmpayment/<int:id>',views.confirm,name="confirmpayment"),
    path('chat/<int:id>',views.chat,name="chat"),
    path('deleteproduct/<int:id>',views.delete_product,name="deleteproduct"),
    path('chatt/<int:id>',views.chatt,name="chatt"),
    

    #customer#
    path('customerprofile',views.customer_profile,name="customerprofile"),
    path('edicustomer',views.edit_customer,name="edicustomer"),
    path('purchase',views.purchase,name="purchase"),
    path('cart',views.cart_view,name="cart"),
    path('viewproduct',views.view_product,name="viewproduct"),
    path('productsearch',views.product_search,name="productsearch"),
    path('productbooking/<int:id>',views.product_booking,name="productbooking"),
    path('myorders',views.my_orders,name="myorders"),
    path('payment/<int:id>',views.payment,name="payment"),
    path('confirmpaymentcustomer/<int:id>',views.confirm_payment,name="confirmpaymentcustomer"),
    path('cashondelivery/<int:id>',views.cash_on_delivery,name="cashondelivery"),
    path('vieworders',views.view_orders,name="vieworders"),
    path('addtocart/<int:id>',views.add_to_cart,name="addtocart"),
    path('cartdelete/<int:id>',views.cart_delete,name="cartdelete"),
    path('cartbooking',views.cart_booking,name="cartbooking"),
    path('send_message/<int:sender_id>/<int:receiver_id>/',views.send_message,name="send_message"),
    path('chatseller/<int:product_id>',views.chat_seller,name="chatseller"),
    path('deleteorder/<int:id>',views.delete_order,name="deleteorder"),
    path('add__product',views.add__product,name="add__product"),
    path('edit__product/<int:id>',views.edit__product,name="edit__product"),
    path('seller__viewproducts',views.seller__viewproducts,name="seller__viewproducts"),
    path('delete__product/<int:id>',views.delete__product,name="delete__product"),
    path('seller__viewbookings',views.seller__viewbookings,name="seller__viewbookings"),   
    path('booking__status/<int:id>',views.booking__status,name="booking__status"),
    path('confirmm/<int:id>',views.confirmm,name="confirmm"),


    #hospital#
    path('hospitalprofile',views.hospital_profile,name="hospitalprofile"),
    path('edithospital',views.edit_hospital,name="edithospital"),
    path('addparent',views.add_parent,name="addparent"),
    path('addbaby/<int:id>',views.add_baby,name="addbaby"),
    path('addnutritionist',views.add_nutritionist,name="addnutritionist"),
    path('viewnutritionist',views.view_nutritionist,name="viewnutritionist"),
    path('deletenutritionist/<int:id>',views.delete_nutritionist,name="deletenutritionist"),
    path('adddoctordetails',views.add_doctor_details,name="adddoctordetails"),
    path('viewparents',views.view_parent,name="viewparents"),
    path('searchparent',views.search_parent,name="searchparent"),
    path('editdoctordetails/<int:id>',views.edit_doctor,name="editdoctordetails"),
    path('viewbabyh/<int:id>',views.view_baby,name="viewbabyh"),
    path('viewdoctorlist',views.view_doctor,name="viewdoctorlist"),
    path('searchdoctor',views.search_doctor,name="searchdoctor"),
    path('deletedoctor/<int:id>',views.delete_doctor,name="deletedoctor"),
    path('deleteparent/<int:id>',views.delete_parent,name="deleteparent"),
    path('viewappoinment/<int:id>',views.view_appoinment,name="viewappoinment"),
    path('hospitalsearchappt/<int:id>',views.hospital_search_appt,name="hospitalsearchappt"),
    path('addvideos',views.add_videos,name="addvideos"),
    path('viewvideos',views.view_videos,name="viewvideos"),
    path('parentviewvideos',views.pview_videos,name="parentviewvideos"),
    path('editvideos/<int:id>',views.edit_videos,name="editvideos"),
    path('deletevideos/<int:id>',views.delete_videos,name="deletevideos"),
    path('addvaccination',views.add_vaccination,name="addvaccination"),
    path('mainviewvaccine',views.mainview_vaccine,name="mainviewvaccine"),
    path('viewbabyvaccine/<int:id>',views.viewbaby_vaccine,name="viewbabyvaccine"),
    path('vtaken/<int:id>',views.date_vtaken,name="vtaken"),
    

    #nutritionist#
    path('nprofile',views.n_profile,name="nprofile"),
    path('editnutritionist',views.edit_nutritionist,name="editnutritionist"),
    path('viewparentlist',views.nview_parent,name="viewparentlist"),
    path('nviewbaby/<int:id>',views.nview_baby,name="nviewbaby"),
    path('nbabyvaccine/<int:id>',views.nbaby_vaccine,name="nbabyvaccine"),
    path('nsearchparent',views.nsearch_parent,name="nsearchparent"),
    path('parentmsg/<int:id>',views.parent_msg,name="parentmsg"),
    path('chatlist',views.chat_list,name="chatlist"),

    #parent#
    path('parentprofile',views.parent_profile,name="parentprofile"),
    path('babydetails',views.baby_details,name="babydetails"),
    path('editbabydetails',views.edit_baby,name="editbabydetails"),
    path('editparentprofile',views.edit_parent,name="editparentprofile"),
    path('doctorlist',views.doctor_list,name="doctorlist"),
    path('parentsearchdoctor',views.parentsearch_doctor,name="parentsearchdoctor"),
    path('doctorbooking/<int:id>',views.doctor_booking,name="doctorbooking"),
    path('myappoinments',views.my_appoinments,name="myappoinments"),
    path('cancelbooking/<int:id>',views.cancel_booking,name="cancelbooking"),
    path('vaccinationchart/<int:id>',views.vaccination_chart,name="vaccinationchart"),
    path('add_vdocument/<int:id>',views.add_vdocument,name="add_vdocument"),
    path('pviewvideos',views.pview_videos,name="pviewvideos"),
    path('chatnutritionist',views.chat_nutritionist,name="chatnutritionist"),
    path('msg',views.msg,name="msg"),
    path('list',views.list,name="list"),
    path('purchaseee',views.purchaseee,name="purchaseee"),
    path('product__search',views.product__search,name="product__search"),
    path('add__tocart/<int:id>',views.add__tocart,name="add__tocart"),
    path('cart___view',views.cart___view,name="cart___view"),
    path('cart__delete/<int:id>',views.cart__delete,name="cart__delete"),
    path('cart__booking',views.cart__booking,name="cart__booking"),
    path('product__booking/<int:id>',views.product__booking,name="product__booking"),
    path('my__orders',views.my__orders,name="my__orders"),
    path('delete__order/<int:id>',views.delete__order,name="delete__order"),
    path('paymentt/<int:id>',views.paymentt,name="paymentt"),
    path('confirm__payment/<int:id>',views.confirm__payment,name="confirm__payment"),
    path('cash__on__delivery/<int:id>',views.cash__on__delivery,name="cash__on__delivery"),
    path('chat__seller/<int:product_id>',views.chat__seller,name="chat__seller"),
    

    # admin #

    path('admin/',admin.site.urls),
    path('adminhome',views.admin_home,name="adminhome"),
    path('admincustomer',views.admin_customer,name="admincustomer"),
    path('adminhospital',views.hospital_view,name="adminhospital"),
    path('hospitalsearch',views.hospital_search,name="hospitalsearch"),
    path('adminseller',views.admin_seller,name="adminseller"),
    path('status/<int:id>',views.admin_approval,name="status"),
    
   
    
    
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
