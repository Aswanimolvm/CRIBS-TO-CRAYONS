from django.contrib import admin
from .models import Seller,Customer,Hospital,LoginUser

# Register your models here.
admin.site.register(Seller)
admin.site.register(Customer)
admin.site.register(Hospital)
admin.site.register(LoginUser)