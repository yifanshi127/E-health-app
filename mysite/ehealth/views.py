from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, QueryDict
from .models import HealthData,Person
from .forms	import CreatNewPerson,UpdatePerson
from .signal import *
from django.contrib import messages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import time


# set default user and person in case the user forget to create
try:
	u = User.objects.create(username="guset",password="1DS8ylMMP")
	p = Person.objects.create(user=u,name="guest",age=10,gender="Male",personalheight=160,personalweight=50)
except IntegrityError:
	u = User.objects.filter(username="guest")
	p = Person.objects.filter(name="guest")

def index(request, id):
	global p
	try:
		p = Person.objects.get(id = id)
		if p in request.user.person.all():
			return render(request,"ehealth/healthdata.html", {"person": p})
	except Person.DoesNotExist:
		messages.warning(request,'You do not have permission to access those records.')
		return HttpResponseRedirect("/ehealth/history")
	return render(request, "ehealth/history.html", {})

def home(request):
	try:
		user = str(request.user)
		global p
		p = Person.objects.get(name=user)
	except Person.DoesNotExist:
		messages.warning(request,'You have to login first.')
		return HttpResponseRedirect("/ehealth/login")
	return render(request, "ehealth/home.html",{"person": p})


def create(request):
	user = str(request.user)
	if request.method == "POST":
		form = CreatNewPerson(request.POST)

		if form.is_valid():
			name = form.cleaned_data["name"]
			age = form.cleaned_data["age"]
			gender = form.cleaned_data["gender"]
			personalheight = form.cleaned_data["personalheight"]
			personalweight = form.cleaned_data["personalweight"]
			if name == user:
				global p
				p = Person(name=name,age=age,gender=gender,personalheight=personalheight,personalweight=personalweight)
				try:
					p.save()
					request.user.person.add(p)
				except IntegrityError:
					messages.warning(request,'You have already added your information.')
					p.delete()
					return HttpResponseRedirect("/ehealth/create")
			else:
				messages.warning(request,'Please fill in your username correctly.')
				return HttpResponseRedirect("/ehealth/create")
		return HttpResponseRedirect("/ehealth/%i" %p.id)
	else:
		form = CreatNewPerson()
	return render(request, "ehealth/create.html", {"form":form})


def user(request):
	try:
		user = str(request.user)
		global p
		p = Person.objects.get(name=user)
	except ObjectDoesNotExist:
		messages.warning(request,'Please fill in your information first.')
		return HttpResponseRedirect("/ehealth/create")
	except MultipleObjectsReturned:
		p = Person.objects.filter(name=user)
		p[0].delete()
		p = Person.objects.get(name=user)
	return render(request, "ehealth/user.html",{"person":p})

def update(request):
	user = str(request.user)
	if request.method == "POST":
		form = UpdatePerson(request.POST)
		if form.is_valid():
			global p
			name = form.cleaned_data["name"]
			age = form.cleaned_data["age"]
			gender = form.cleaned_data["gender"]
			personalheight = form.cleaned_data["personalheight"]
			personalweight = form.cleaned_data["personalweight"]
			if name == user:
				p = Person.objects.filter(name=user).update(name=name,age=age,gender=gender,personalheight=personalheight,personalweight=personalweight)
			else:
				messages.warning(request,'Please fill in your username correctly.')
				return HttpResponseRedirect("/ehealth/update")
		return HttpResponseRedirect("/ehealth/user")
	else:
		form = UpdatePerson()
	return render(request, "ehealth/update.html", {"form":form})


def history(request):
	try:
		user = str(request.user)
		if user == "AnonymousUser":
			messages.warning(request,'You have to login first.')
			return HttpResponseRedirect("/ehealth/login")
		global p
		p = Person.objects.get(name=user)
	except ObjectDoesNotExist:
		messages.warning(request,'Please fill in your information first.')
		return HttpResponseRedirect("/ehealth/create")
	except MultipleObjectsReturned:
		p = Person.objects.filter(name=user)
		p[0].delete()
		p = Person.objects.get(name=user)
	return render(request, "ehealth/history.html", {})

def insertion(request):
	try:
		message = "Recording..."
		print('med' in request.GET)
		global p
		if 'med' in request.GET:
			med = request.GET.get('med')
			femg = request.GET.getlist('femg')
			emg = request.GET.getlist('emg')
			temp = request.GET.get('temp')
			plus = request.GET.get('plus')
			spo = request.GET.get('spo')
			fati = request.GET.get('fati')
			h = HealthData(person=p,originalEMG=emg,frequencyEMG=femg,mediafreq=med,temperature=temp ,spO2=spo, pulse=plus, fati=fati)
			h.save()
			print(med)
			print(femg)
			print(emg)
			print(plus)
			print(spo)
			print(fati)
		else:
			h = HealthData()
	except Person.DoesNotExist:
		messages.warning(request,'You have not added your information,please add them.')
		return HttpResponseRedirect("/ehealth/create")
	return render(request,'ehealth/insertion.html',{"message":message, "person":p})


# --ABANDONED FUNCTIONS--
# def button(request):
# 	return render(request,'ehealth/home.html')
#
# def switch(request):
# 	if request.method == "POST":
# 		form = SwitchPerson(request.POST)
# 		if form.is_valid():
# 			name = form.cleaned_data["name"]
# 			#global p
# 			p = Person.objects.get(name=name)
# 		return HttpResponseRedirect("/ehealth")
# 	else:
# 		form = SwitchPerson()
# 	return render(request,"ehealth/switch.html",{"form":form})

#   def clearhistory(request):
# 	#global p
# 	p.healthdata_set.all.delete()
# 	return render(request, "ehealth/history.html", {})

#  def insertion(request):
	# user = request.user
	# print(user)
	# #global p
	# p = Person.objects.get(name=user)
	# h = HealthData(person = p, originalEMG = getemg().tolist(),temperature = gettem() ,spO2 = getspo(), pulse = getplu())
	# print(h)
	# h.save()
	# #global pauseinsertion
	# pauseinsertion = False
	# while True:
	# time.sleep(3)
	# 	if pauseinsertion is True:

# def pauseinsertion(request):
# 	print("pause")
# 	#global pauseinsertion
# 	pauseinsertion = True
# 	return render(request,'ehealth/home.html')

# def runmonitor(response):
# 	out = run([sys.executable,'//Users//yifanshi//mysite//ehealth//scripts//monitor.py'],shell=False,stdout=PIPE)
# 	print(out)
# 	return render(response,'home.html',{'data':out})
