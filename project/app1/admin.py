from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User,Hospital,LoginUser, Parent,Booking,Productbooking,Vaccination,Video,Baby_details,Cart,Nutritionist,Doctor,Baby_vaccine,Product,Chat


# class seller(admin.ModelAdmin):
#     list_display = ('seller_name', 'Email','phone')
#     # list_filter = ('status')
#     readonly_fields = ('seller_name','Email','street','district','pincode','phone','login_id')
#     search_fields = ('seller_name',)
class user(admin.ModelAdmin):
    list_display = ('user_name','Email','phone')
    readonly_fields = ('user_name','Email','street','district','pincode','phone','login_id')
    search_fields = ('user_name',)
class hospital(admin.ModelAdmin):
    list_display = ('hospital_name','Email','phone')
    readonly_fields = ('hospital_name','Email','street','district','pincode','phone','licence_proof','login_id')
    search_fields = ('hospital_name',)
class parent(admin.ModelAdmin):
    list_display = ('parent_name','Email','phone')
    readonly_fields = ('parent_name','Email','street','district','pincode','phone','hospital_id','login_id')
    search_fields = ('parent_name',)
class nutritionist(admin.ModelAdmin):
    list_display = ('Nutritionist_name','hospital_id')
    readonly_fields = ('Nutritionist_name','consulting_days','consulting_time','hospital_id','login_id')
    search_fields = ('Nutritionist_name',)
class users(admin.ModelAdmin):
    list_display = ('username','user_type','status')
    search_fields = ('username',)
    list_filter = ('status','user_type')
    list_per_page = 10
    fieldsets = [
        (None, {"fields": ["username", "user_type", "status"]}),
        
    ]


# Register your models here.
# admin.site.register(Seller,seller)
admin.site.register(User,user)
admin.site.register(Hospital,hospital)
admin.site.register(LoginUser,users)
admin.site.register(Parent,parent)
admin.site.register(Nutritionist,nutritionist)
admin.site.register(Doctor)
admin.site.register(Booking)
admin.site.register(Productbooking)
admin.site.register(Vaccination)
admin.site.register(Video)
admin.site.register(Baby_vaccine)
admin.site.register(Product)
admin.site.register(Baby_details)
admin.site.register(Cart)
admin.site.unregister(Group)
admin.site.register(Chat)
admin.site.site_header='CRIBS TO CRAYONS'