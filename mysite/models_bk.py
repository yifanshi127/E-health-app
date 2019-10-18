from django.db import models
from django.utils.timezone import now
# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=200, blank=True, null=True)
	age = models.IntegerField()
	gender = models.CharField(max_length=10, blank=True, null=True)
	personalheight = models.IntegerField()
	personalweight = models.IntegerField()


class HealthData(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	rec_date = models.DateTimeField(auto_now_add=True, blank=True)
	originalEMG = models.IntegerField()
	frequencyEMG = models.IntegerField()
	medianfrequency = models.IntegerField()
	temperature = models.IntegerField()
	spO2 = models.IntegerField()
	pulse = models.IntegerField()
