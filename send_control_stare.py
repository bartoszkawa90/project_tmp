from serial import Serial
import numpy as np


# EXAMPLE SIN CONTROL   [ nuta, time, ... ]
# nuta = 0 , freq = 350Hz(dolne c)    , nuta = 7 , freq = 704Hz(górne c)
# time = 1 , czas = 8s     , time = 2 , czas = 4s    , time = 8 , czas = 1s
all_nutes = [0,8, 1,8, 2,8, 3,8, 4,8, 5,8, 6,8, 7,8]

# cwircnuta to chyba jednak pol sekundy
#wlazl_kotek = [5,8, 3,8, 3,8, 4,8, 2,8, 2,8,    1,16, 3,16, 5,8, 5,8, 3,8, 3,8,    4,8, 2,8, 2,8, 1,16, 3,16, 1,4,    1,8, 3,8, 3,8, 2,8, 4,8, 4,8,    1,16, 3,16, 5,4, 5,8, 3,8, 3,8]
wlazl_kotek = [5,16, 3,16, 3,16, 4,16, 2,16, 2,16,    1,32, 3,32, 5,8, 5,16, 3,16, 3,16,    4,16, 2,16, 2,16, 1,32, 3,32, 1,8,    1,16, 3,16, 3,16, 2,16, 4,16, 4,16,    1,32, 3,32, 5,8, 5,16, 3,16, 3,16,   7,2]
print(len(wlazl_kotek))
#songs = {}


b_control = bytes(wlazl_kotek)

ser = Serial("COM3", 28800)
play = b'\xcc\x01\x3e\x0a'   # send   >  /play
back_to_begining = b'\xcc\x01\x21\x0a'   # send   !  /go back to the begining of the song 
stop = b'\xcc\x01\x7c\x0a'   # send   |  /stop
clear_all = b'\xcc\x01\x21\x21\x21\x0a' # send !!! / clear all song data


# RESPONSE FROM SOURCE
ser.write(b'\x0c')
print("Checking connection ... ")
ser.write(b'\x0c')
ser.write(b'\x0c')
while(True):
    ser.write(b'\x0c')
    check = ser.read(16)
    if check[0] : print("   Received something")
    if check.decode() == "Connection works":
        print("   " + check.decode() + " ")
        break
    ser.write(b'\x0c')



# CONTROL
while (True):
    choice = input(" Select to send signal data signal or  give some command ")
    
    if choice == "play":
        ser.write(play)

    elif choice == "send":
        ser.write(b'\x01')
        ser.write(b_control)
        ser.write(b'\x0a')

    elif choice == "clear":
        ser.write(clear_all)

    elif choice == "stop":
        ser.write(stop)

    elif choice == "back to beginning":
        ser.write(back_to_begining)
        
    else:
        print(" Wrong command ")
        
