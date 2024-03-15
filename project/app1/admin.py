from django.contrib import admin
from .models import Seller,Customer,Hospital,LoginUser, Parent,Booking,Productbooking

# Register your models here.
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Hospital)
admin.site.register(LoginUser)
admin.site.register(Parent)
admin.site.register(Booking)
admin.site.register(Productbooking)