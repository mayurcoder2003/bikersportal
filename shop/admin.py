from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Orders, OrderUpdate, BookMechanic, User_Signup

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(BookMechanic)
admin.site.register(User_Signup)