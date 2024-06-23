from django.contrib import admin

from main_app.models import Customer


# Register your models here.
@admin.register(Customer)
class Customer(admin.ModelAdmin):
    pass