from django.db import models

# Create your models here.

class Person(models.Model):
	name = models.CharField(max_length=200)
	age = models.IntegerField()

class HealthData(models.Model):
	person = models.ForeignKey(Person, on_delete=models.CASCADE)
	data = models.CharField(max_length=500)
	rec_date = models.DateTimeField('recorded')

