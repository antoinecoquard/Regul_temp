#!/usr/bin/env python
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
with open('suivitemp.txt', 'a') as f: #creation du fichier a modifier pour controler le repertoir
        f.write( 'importation demarre le:') #en tête qui se refait en cas de redemarage (3 lignes)
        f.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
        f.write('\n')
        f.write( 'date et heure,temp_in,temp_ext,statut_fan,statut_chauff,press, humidity\n')
        f.write( 'yyyy-mm-dd hh:mm:ss,degC,degC,ss,ss,hPa,%\n')
print 'date et heure,temp_in,temp_ext,statut_fan,statut_chauff,press, humidity\n' #pour verifier le deroulement en mode terminal

while True: #début de la boucle 5min
    os.system('sudo /home/pi/suivitemp/Dropbox-uploader/dropbox_uploader.sh upload /home/pi/suivitemp.txt /suivitemp') #tape la ligne de cmd pour uploader sur dropbox
    #vide la memoire des enregistrement 5s
    fivemintemp_in = []
    fivemintemp_ext = []
    fiveminstatut_fan = []
    fiveminstatut_chauff = []
    fiveminpress = []
    fiveminhumidity = []
        
    count = 0 #initialise compteur pour s'assurer que 1min est pasé avant de vérifier si le nb de min est un multiple de 5
    
    while count < 20 or (datetime.datetime.now().minute)%5 != 0: # boucle tant que est vrai une des deux conditions (nb de mesure inf à 20 / le nb de min n'est pas multiple de 5)
        data = ser.readline() #lecture du port serie
        temp_in, temp_ext, statut_fan, statut_chauff, press, humidity = data.split(',') #décode les lectures 5s
        fivemintemp_ext.append(float(temp_in)) #stock dans un tableau les lectures 5s
        fivemintemp_in.append(float(temp_ext))
        fiveminstatut_fan.append(float(statut_fan))
        fiveminstatut_chauff.append(float(statut_chauff))
        fiveminpress.append(float(press))
        fiveminhumidity.append(float(humidity))
        count = count+1
        print (datetime.datetime.now().minute)%5 #pour verifier le deroulement en mode terminal
        print count
        print fivemintemp_in
        #fin de la boucle 5s
        
    # calcul des moyennes 5 min
    temp_in = sum(fivemintemp_in) / float(len(fivemintemp_in))
    temp_ext = sum(fivemintemp_ext) / float(len(fivemintemp_ext))
    statut_fan = sum(fiveminstatut_fan) * float(5)
    statut_chauff = sum(fiveminstatut_chauff) * float(5)
    press = sum(fiveminpress) / float(len(fiveminpress))
    humidity = sum(fiveminhumidity) / float(len(fiveminhumidity))
   

    with open('suivitemp.txt', 'a') as f: #écrit les moyenne 5 min sur le fichier txt arrdoni avec 1 chiffre aprés la virgule
        f.write('{},{},{},{},{},{},{}\n'.format(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')),
                                  Decimal(str(round(temp_in,1))),
                                  Decimal(str(round(temp_ext,1))),
                                  Decimal(str(round(statut_fan,1))),
                                  Decimal(str(round(statut_chauff,1))),
                                  Decimal(str(round(press,1))))) 
                                  Decimal(str(round(humidity,1))),
