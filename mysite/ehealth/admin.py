from django.contrib import admin
from .models import HealthData
from .models import Person
# Register your models here.
admin.site.register(HealthData)
admin.site.register(Person)
