t#!/usr/bin/env python
import datetime
import serial
import time
import os
from decimal import Decimal

ser = serial.Serial(
    port='/dev/ttyACM0', #port usb sur Pi à changer si PC
    baudrate = 9600 #baudrate du port serie
)

ser.readline() #pour debug
time.sleep(5)
ser.readline() #fin du debug
with open('/home/pi/suivimet/datalog.txt', 'a') as f: #creation du fichier
        f.write( 'importation demarre le:') #en tête qui se refait en cas de redemarage (3 lignes)
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
        f.write('\n')
        f.write( 'date,wd,ws,temp_ext\n')
        f.write( 'yyyy-mm-dd hh:mm:ss,deg,km/h,DegC\n')
print 'datalogOK\n' #pour verifier le deroulement en mode terminal

while True: #début de la boucle 5min
    
    fivemintemp_wd = []
    fivemintemp_ws = []
    fiveminstatut_temp = []
    #fiveminstatut_chauff = []
    #fiveminpress = []
    #fiveminhumidity = []
        
    count = 0 #initialise compteur pour s'assurer que 1min est pasé avant de vérifier si le nb de min est un multiple de 5
    
    while count < 15 or (datetime.datetime.now().minute)%4 != 0: # boucle tant que est vrai une des deux conditions (nb de mesure inf à 20 / le nb de min n'est pas multiple de 5)
        data = ser.readline() #lecture du port serie
        wd, ws, temp = data.split(',') #décode les lectures 5s
        #fivemintemp_wd.append(float(wd)) #stock dans un tableau les lectures 5s
        fivemintemp_wd.(float(wd))
        fivemintemp_ws.append(float(ws))
        fiveminstatut_temp.append(float(temp))
        
        count = count+1
        print datetime.datetime.now() #pour verifier le deroulement en mode terminal
        print count
        print fivemintemp_ws
        print fivemintemp_wd
        #fin de la boucle 5s
        
    # calcul des moyennes 5 min
    wd = sum(fivemintemp_wd) / float(len(fivemintemp_wd))
    ws = sum(fivemintemp_ws) / float(len(fivemintemp_ws))
    temp = sum(fivemin_temp) / float(len(fivemin_temp))


    with open('/home/pi/suivimet/suivimet.txt', 'a') as f: #écrit les moyenne 5 min sur le fichier txt arrondi avec 1 chiffre aprés la virgule
        f.write('{},{},{},{}\n'.format(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                                  Decimal(str(round(wd,0))),
                                  Decimal(str(round(ws,1))),
                                  Decimal(str(round(temp,1)))),
                
 
