from django.shortcuts import render,get_object_or_404,redirect
# Create your views here.

from django.http import HttpResponse
import datetime

def cur_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" %now
    return HttpResponse(html)


# h = HealthData(PersonID='1',DataId='')
	# PersonID = models.ForeignKey(Person, on_delete=models.CASCADE)
	# DataID = models.IntegerField()
	# Rec_date = models.DateTimeField('recorded')
	# OriginalEMG = models.IntegerField()
	# FrequencyEMG = models.IntegerField()
	# Medianfrequency = models.IntegerField()
	# Temperature = models.IntegerField()
	# SPO2 = models.IntegerField()
	# Pulse = models.IntegerField()
