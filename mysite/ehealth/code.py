from ehealth.signal import *
from ehealth.models import Person,HealthData
from django.utils import timezone
import time

def createperson():
    p = Person(name = "yifanshi", age = "24", gender = "Male", personalheight = "183", personalweight = "70")
    p.save()

def insertrecord():
    h = HealthData(person = p, originalEMG = getemg().tolist(),temperature = gettem() ,spO2 = getspo(), pulse = getplu())
    h.save()

def loopinsert():
    while True:
        insertrecord()
        time.sleep(1)

#def stopcontrol():



#feature: a)run insert records every 5 seconds
#feature: b)stop record
#a control bottom on the webpage to start/stop
#function retrieve data from the databases
