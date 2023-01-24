from serial import Serial


# PRZYKŁAD KONTROLI GRANIA SINUSEM   [ nuta, time, ... ]
# nuta = 0 , freq = 350Hz(dolne c)    , nuta = 7 , freq = 704Hz(górne c)
# time = 1 , czas = 8s     , time = 2 , czas = 4s    , time = 8 , czas = 1s
gama = [1,8, 2,8, 3,8, 4,8, 5,8, 6,8, 7,8, 8,8]
wlazl_kotek = [5,16, 3,16, 3,16, 4,16, 2,16, 2,16,    1,32, 3,32, 5,8, 5,16, 3,16, 3,16,    4,16, 2,16, 2,16, 1,32, 3,32, 1,8,    1,16, 3,16, 3,16, 2,16, 4,16, 4,16,    1,32, 3,32, 5,8, 5,16, 3,16, 3,16]
panie_janie = [4,16, 5,16, 6,16, 4,16, 4,16, 5,16, 6,16, 4,16,     6,16, 7,16, 8,8, 6,16, 7,16, 8,8,    8,32, 2,32, 8,32, 7,32, 6,16, 4,16, 8,32, 2,32, 8,32, 7,32, 6,16, 4,16,    5,16, 1,16, 4,8, 5,16, 1,16, 4,8]


print("1 Rozmiar " , len(wlazl_kotek) , "   2 Rozmiar " , len(panie_janie))
songs = {"wlazl kotek" : wlazl_kotek , "panie janie" : panie_janie}

# KOMENDY
print("Komendy : " + "\n" + " play - zagranie wysłaną piosenką" + "\n" + " clear - wyczyszczenie tablicy sygnału na płytce" + "\n" + " send <nazwa_piosenki lub jej pozycja w tablicy> - wysłanie piosenki na płytkę" 
      + "\n" + " stop - zatrzymanie aktualnie granej piosenki" + "\n" +  " back to beginning - powrót na początek piosenki")

print("\nPiosenki : ")
for i in songs.keys(): print(" ", i)


# Komendy
play = b'\xcc\x0f\x3e\x0a'   # send   >  /play
back_to_begining = b'\xcc\x0f\x21\x0a'   # send   !  /go back to the begining of the song 
stop = b'\xcc\x0f\x7c\x0a'   # send   |  /stop
clear_all = b'\xcc\x0f\x21\x21\x21\x0a' # send !!! / clear all song data

ser = Serial("COM3", 28800)

# Odpowiedź
ser.write(b'\x0c')
print("\nChecking connection ... ")
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


# Kontrola // komendy i wysyłanie sygału
while (True):
    choice = input(" Select to send signal data signal or  give some command ")
    
    if choice == "play":
        ser.write(play)

    elif choice.split(' ')[0] == "send":
        try:
            ser.write(b'\x0f')
            if (ord(choice[5]) > 47 and ord(choice[5]) < 58):
                print(list(songs.values())[int(choice[5])])
                ser.write(bytes(list(songs.values())[int(choice[5])-1]))
            else:
                print(songs[choice[5:]])
                ser.write(bytes(songs[choice[5:]]))
            ser.write(b'\x0a')
        except:
            print("No song with that name")      

    elif choice == "clear":
        ser.write(clear_all)

    elif choice == "stop":
        ser.write(stop)

    elif choice == "back to beginning":
        ser.write(back_to_begining)
        
    else:
        print(" Wrong command ")

        
