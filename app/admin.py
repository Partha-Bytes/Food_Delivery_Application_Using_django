from django.contrib import admin
from .models import Dish, Menu, Order, Cart , Review

# Register your models here.

admin.site.register(Dish)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Review) 