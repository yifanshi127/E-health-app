from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import HealthData, Person
from .forms	import CreatNewPerson
from .signal import *
import time

# import requests
# from subprocess import run,PIPE

p = Person.objects.get(name="Guest")

def index(response, id):
	person = Person.objects.get(id = id)
	return render(response,"ehealth/healthdata.html",{"person": person})

def home(response):
	data = response.GET['msg_content']
	print(data)
	return render(response, "ehealth/home.html")
# ,{"data": data}
def create(response):
	if response.method == "POST":
		form = CreatNewPerson(response.POST)

		if form.is_valid():
			name = form.cleaned_data["name"]
			age = form.cleaned_data["age"]
			gender = form.cleaned_data["gender"]
			personalheight = form.cleaned_data["personalheight"]
			personalweight = form.cleaned_data["personalweight"]
			global p
			p = Person(name=name,age=age,gender=gender,personalheight=personalheight,personalweight=personalweight)
			p.save()

		return HttpResponseRedirect("/ehealth")
		# return p,HttpResponseRedirect("/ehealth/%i" %p.id)

	else:
		form = CreatNewPerson()
	return render(response, "ehealth/create.html", {"form":form})

def button(response):
	return render(response,'ehealth/home.html')

def insertion(response):
	# global pauseinsertion
	# pauseinsertion = False
	# while True:
	global p
	h = HealthData(person = p, originalEMG = getemg().tolist(),temperature = gettem() ,spO2 = getspo(), pulse = getplu())
	print(h)
	h.save()
	# time.sleep(3)
		# if pauseinsertion is True:
	return render(response,'ehealth/home.html')

def pauseinsertion(response):
	print("pause")
	global pauseinsertion
	pauseinsertion = True
	return render(response,'ehealth/home.html')

# def runmonitor(response):
# 	out = run([sys.executable,'//Users//yifanshi//mysite//ehealth//scripts//monitor.py'],shell=False,stdout=PIPE)
# 	print(out)
# 	return render(response,'home.html',{'data':out})
