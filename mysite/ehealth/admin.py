from django.contrib import admin
from .models import HealthData,Person
from django.contrib.auth.models import  User

# Register your models here.

admin.site.register(HealthData)
admin.site.register(Person)
