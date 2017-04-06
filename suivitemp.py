#!/usr/bin/env python
import datetime
import serial
import time
import os
from decimal import Decimal

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600
)

ser.readline()
time.sleep(5)
ser.readline()
with open('suivitemp.txt', 'a') as f:
        f.write( 'importation demarre le:')
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
        f.write('\n')
        f.write( 'date et heure, press, temp_BMP , humidity, temp_DHT, temp_DS, statut_fan\n')
        f.write( 'yyyy-mm-dd hh:mm:ss,HPa,degC,%,degC,degC,sec\n')
print 'date et heure, press, temp_BMP , humidity, temp_DHT, temp_DS, statut_fan\n'

while True:
    os.system('sudo /home/pi/suivitemp/Dropbox-uploader/dropbox_uploader.sh upload /home/pi/suivitemp.txt /suivitemp')
    fiveminpress = []
    fivemintemp_BMP = []
    fiveminhumidity = []
    fivemintemp_DHT = []
    fivemintemp_DS = []
    fiveminstatut_fan = []
    
    count = 20
    while count > 1 or (datetime.datetime.now().minute)%5 != 0:
        data = ser.readline()
        press, temp_BMP, humidity, temp_DHT, temp_DS, statut_fan = data.split(',')
        fiveminpress.append(float(press))
        fivemintemp_BMP.append(float(temp_BMP))
        fiveminhumidity.append(float(humidity))
        fivemintemp_DHT.append(float(temp_DHT))
        fivemintemp_DS.append(float(temp_DS))
        fiveminstatut_fan.append(float(statut_fan))
        count = count-1
        print temp_DS
        print (datetime.datetime.now().minute)%5
        print fiveminpress
        print count
    press = sum(fiveminpress) / float(len(fiveminpress))
    temp_BMP = sum(fivemintemp_BMP) / float(len(fivemintemp_BMP))
    humidity = sum(fiveminhumidity) / float(len(fiveminhumidity))
    temp_DHT = sum(fivemintemp_DHT) / float(len(fivemintemp_DHT))
    temp_DS = sum(fivemintemp_DS) / float(len(fivemintemp_DS))
    statut_fan = sum(fiveminstatut_fan) * float(5)
    
    with open('suivitemp.txt', 'a') as f:
        f.write('{},{},{},{},{},{},{}\n'.format(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                                  Decimal(str(round(press,1))),
                                  Decimal(str(round(temp_BMP,1))),
                                  Decimal(str(round(humidity,1))),
                                  Decimal(str(round(temp_DHT,1))),
                                  Decimal(str(round(temp_DS,1))),
                                  Decimal(str(round(statut_fan,1))))) 
