from django.contrib import admin
from .models import Seller,Customer,Hospital,LoginUser, Parent,Booking,Productbooking,Vaccination,Video,Baby_details,Cart

# Register your models here.
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Hospital)
admin.site.register(LoginUser)
admin.site.register(Parent)
admin.site.register(Booking)
admin.site.register(Productbooking)
admin.site.register(Vaccination)
admin.site.register(Video)
admin.site.register(Baby_details)
admin.site.register(Cart)