
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 09:50:37 2019
@author: Brown
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from time import sleep

def getemg():
  emg1s = np.random.randint(0,high=1024,size=500)
  return emg1s

def gettem():
  tem = round(random.uniform(30.01,42.00),2)
  return tem

def getplu():
  plu = random.randint(30,250)
  return plu

def getspo():
  spo = random.randint(90,100)
  return spo

def emgfft(emgsignal):
  fftsignal = np.fft.rfft(emgsignal)
  fftsignal = fftsignal[1:251] # remove the DC part
  return fftsignal

def mediafreq(fftemg):
  m = fftemg.__add__(abs (fftemg.min()))
  t = np.sum(m) /2 #half product
  k = 0  #sum
  s = [] # sub
  for i in range (len(m)):
      k = k+ m[i] # current sum
      s.append(abs(t-k))
  med = s.index(min(s))
  return med

def showpic(rawemg, freqemg,media):
  fig=plt.figure(num=3,figsize= [35,20],clear=1)
  ax=fig.add_subplot(2,1,1)
  ax1=fig.add_subplot(2,1,2)
  ax.set_ylabel('Strength')
  ax.set_title('Raw EMG Signals')
  ax1.set_ylabel('Strangth')
  ax1.set_title('Frequency Domain EMG Signals')
  plt.ion()
  plt.grid(True)
  timeline0 = np.arange(500)
  timeline1 = np.arange(250)
  ax.plot(timeline0,rawemg)
  ax1.plot(timeline1,freqemg)
  ax1.axvline(x=media,linewidth=3,color='r')


if __name__ == '__main__':
  emg = getemg()
  freqemg = emgfft(emg)
  media = mediafreq(freqemg)
  showpic(emg,freqemg,media)
