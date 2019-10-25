from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict
from .models import HealthData,Person
from .forms	import CreatNewPerson,SwitchPerson
from .signal import *
from django.contrib import messages
from django.db import IntegrityError
import time
# import requests


# from subprocess import run,PIPE

# p = Person.objects.get(name="Guest")
pauseinsertion = True

def index(request, id):
	p = Person.objects.get(id = id)
	if p in request.user.person.all():
		return render(request,"ehealth/healthdata.html", {"person": person})
	return render(request, "ehealth/history.html", {})

def home(request):
		# "emg","temp","plus","spo"
	return render(request, "ehealth/home.html")
	# ,{"data": data})


def create(request):
	if request.method == "POST":
		form = CreatNewPerson(request.POST)

		if form.is_valid():
			# form.instance.user = Person.objects.get(user=self.request.user)
			name = form.cleaned_data["name"]
			age = form.cleaned_data["age"]
			gender = form.cleaned_data["gender"]
			personalheight = form.cleaned_data["personalheight"]
			personalweight = form.cleaned_data["personalweight"]
			p = Person(name=name,age=age,gender=gender,personalheight=personalheight,personalweight=personalweight)
			try:
				p.save()
				request.user.person.add(p)
			except IntegrityError:
				messages.warning(request,'You have already added your information.')
				p.delete()
				return redirect("/ehealth/create")
		return HttpResponseRedirect("/ehealth/%i" %p.id)
		# return p,HttpResponseRedirect("/ehealth/%i" %p.id)
	else:
		form = CreatNewPerson()
	return render(request, "ehealth/create.html", {"form":form})

# def button(request):
# 	return render(request,'ehealth/home.html')
#
def switch(request):
	if request.method == "POST":
		form = SwitchPerson(request.POST)
		if form.is_valid():
			name = form.cleaned_data["name"]
			global p
			p = Person.objects.get(name=name)

		return HttpResponseRedirect("/ehealth")
	else:
		form = SwitchPerson()
	return render(request,"ehealth/switch.html",{"form":form})

def history(request):
	return render(request, "ehealth/history.html", {})

def insertion(request):
	global pauseinsertion
	global p
	pauserinsertion = not pauseinsertion
	print(pauserinsertion)
	if pauseinsertion is False:
		print("ok")
		if request.method == "GET":
			med = request.GET.get('med')
			femg = request.GET.getlist('femg')
			emg = request.GET.getlist('emg')
			temp = request.GET.get('temp')
			plus = request.GET.get('plus')
			spo = request.GET.get('spo')
			h = HealthData(person=person,originalEMG=emg,freqemg=femg,mediafreq=med,temperature=temp ,spO2=spo, pulse=plus)
			h.save()
			print(med)
			print(femg)
			print(emg)
			print(plus)
			print(spo)
		return render(request,'ehealth/home.html')
	else:
		h = HealthData()
	return render(request,'ehealth/home.html') #do nothing to resquests - need confirm

	# h = HealthData(person = p, originalEMG = getemg().tolist(),temperature = gettem() ,spO2 = getspo(), pulse = getplu())
	# print(h)
	# h.save()
	# global pauseinsertion
	# pauseinsertion = False
	# while True:
	# time.sleep(3)
		# if pauseinsertion is True:

#change the originalEMG temperature spO2 pulse
#		 -> originalEMG,temperature,spO2,pulse = request.GET['xx']


# def pauseinsertion(request):
# 	print("pause")
# 	global pauseinsertion
# 	pauseinsertion = True
# 	return render(request,'ehealth/home.html')

# def runmonitor(response):
# 	out = run([sys.executable,'//Users//yifanshi//mysite//ehealth//scripts//monitor.py'],shell=False,stdout=PIPE)
# 	print(out)
# 	return render(response,'home.html',{'data':out})
