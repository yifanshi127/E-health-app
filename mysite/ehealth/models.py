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

	#user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
	# def __str__(self):
	# 	return self.name

class HealthData(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	rec_date = models.DateTimeField(auto_now_add=True)
	originalEMG = ArrayField(models.FloatField())
	frequencyEMG = ArrayField(models.FloatField())
	mediafreq = models.IntegerField()
	temperature = models.FloatField()
	spO2 = models.IntegerField()
	pulse = models.IntegerField()

	# def __str__(self):
	# 	return self.rec_date


#Even if your Web site is available in only one time zone, it’s still good practice to store data in UTC in your database. The main reason is Daylight Saving Time (DST). Many countries have a system of DST, where clocks are moved forward in spring and backward in autumn. If you’re working in local time, you’re likely to encounter errors twice a year, when the transitions happen.
