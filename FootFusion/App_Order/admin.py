from django.contrib import admin

# Register your models here.
from App_Order.models import Order,Cart

admin.site.register(Order)
admin.site.register(Cart)