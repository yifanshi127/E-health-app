#！ /usr/bin/env python
import sys
sys.path.insert(0,'../')

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'ehealth.settings'

import django
django.setup()

from django.http import HttpResponse
from django.utils import timezone
from ehealth.signal import *
from ehealth.models import Person,HealthData
from ehealth.views import create
import time

def insertrecord():
    p = create()[0]
    h = HealthData(person = p, originalEMG = getemg().tolist(),temperature = gettem() ,spO2 = getspo(), pulse = getplu())
    h.save()

def loopinsert():
    while True:
        insertrecord()
        time.sleep(3)

def stopinsert():


if __name__ == '__main__':
    loopinsert()

#def stopcontrol():

#feature: a)run insert records every 5 seconds
#feature: b)stop record
#a control bottom on the webpage to start/stop
#function retrieve data from the databases
