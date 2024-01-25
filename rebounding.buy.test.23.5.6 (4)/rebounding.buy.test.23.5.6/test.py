import random
from PyQt5.QtCore import QTime
from PyQt5.QtTest import *

time = QTime.currentTime()
time = time.toString("hh:mm:ss")
time2 = "14:54:30"


timeVar = QTime.fromString("15:00:30","hh:mm:ss")

print(time)


while True:
    if time == timeVar:
        print("111111111111111111")
    else:
        print("기달")
