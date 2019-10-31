from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.

class Person(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='person', unique=True, null=True)
	name = models.CharField(max_length=200)
	age = models.IntegerField()
	gender = models.CharField(max_length=10)
	personalheight = models.IntegerField()
	personalweight = models.IntegerField()
	def get_absolute_url(self):
		return "/ehealth/%i/" %self.id

	#--ABANDONED ATTRIBUTES--
	#user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	# def __str__(self):
	# 	return self.name

class HealthData(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	rec_date = models.DateTimeField(auto_now_add=True)
	originalEMG = ArrayField(models.FloatField())
	frequencyEMG = ArrayField(models.FloatField())
	mediafreq = models.IntegerField()
	temperature = models.FloatField(null=True)
	spO2 = models.IntegerField(null=True)
	pulse = models.IntegerField(null=True)
	fati = models.IntegerField(null=True)
	
	# --ABANDONED FUNCITONS--
	# def __str__(self):
	# 	return self.rec_date
