from django.db import models
from django.utils.timezone import now
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=200, blank=True, null=True)
	age = models.IntegerField()
	gender = models.CharField(max_length=10, blank=True, null=True)
	personalheight = models.IntegerField()
	personalweight = models.IntegerField()


class HealthData(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	rec_date = models.DateTimeField(auto_now_add=True, editable=True)
	originalEMG = ArrayField(models.IntegerField())
	temperature = models.FloatField()
	spO2 = models.IntegerField()
	pulse = models.IntegerField()

#Even if your Web site is available in only one time zone, it’s still good practice to store data in UTC in your database. The main reason is Daylight Saving Time (DST). Many countries have a system of DST, where clocks are moved forward in spring and backward in autumn. If you’re working in local time, you’re likely to encounter errors twice a year, when the transitions happen.
