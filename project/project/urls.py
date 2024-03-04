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
    path('',views.home,name="home"),
    path('sellerreg',views.seller_register,name="sellerreg"),
    path('customerreg',views.customer_register,name="customerreg"),
    path('hospitalreg',views.hospital_register,name="hospitalreg"),
    path('login',views.loginpage,name="login"),
    path('sellerprofile',views.seller_profile,name="sellerprofile"),
    path('customerprofile',views.customer_profile,name="customerprofile"),
    path('hospitalprofile',views.hospital_profile,name="hospitalprofile"),
    path('purchase',views.purchase,name="purchase"),
    path('edicustomer',views.edit_customer,name="edicustomer"),
    path('about',views.about,name="about"),
    path('edithospital',views.edit_hospital,name="edithospital"),
    path('addparent',views.add_parent,name="addparent"),
    path('addbaby',views.add_baby,name="addbaby"),
    path('addnutritionist',views.add_nutritionist,name="addnutritionist"),
    path('nprofile',views.n_profile,name="nprofile"),
    path('parentprofile',views.parent_profile,name="parentprofile"),
    path('babydetails',views.baby_details,name="babydetails"),
    path('editseller',views.edit_seller,name="editseller"),
    path('editbabydetails',views.edit_baby,name="editbabydetails"),
    path('editparentprofile',views.edit_parent,name="editparentprofile"),
    path('addproduct',views.add_product,name="addproduct"),
    path('adddoctordetails',views.doctor_details,name="adddoctordetails")
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
