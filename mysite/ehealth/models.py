from django.db import models

# Create your models here.

class Person(models.Model):
	PersonID = models.IntegerField()
	Name = models.CharField(max_length=200)
	Age = models.IntegerField()
	Gender = models.CharField(max_length=10)
	Personalheight = models.IntegerField()
	Personalweight = models.IntegerField()


class HealthData(models.Model):
	DataID = models.IntegerField()
	PersonID = models.ForeignKey(Person, on_delete=models.CASCADE)
	Rec_date = models.DateTimeField('recorded')
	OriginalEMG = models.IntegerField()
	FrequencyEMG = models.IntegerField()
	Medianfrequency = models.IntegerField()
	Temperature = models.IntegerField()
	SPO2 = models.IntegerField()
	Pulse = models.IntegerField()
