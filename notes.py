from serial import Serial
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import random
import struct
import wave

# generating and saving sin values
x = np.linspace(0,2*np.pi,16000
                )
sin = np.sin(x)
SIN = []
for i in range(sin.size):
    if int(255*(sin[i]+1)/2) == 10:
        SIN.append(int(255*(sin[i]+1)/2)+1)
    else:
        SIN.append(int(255*(sin[i]+1)/2))
        
with open(r'C:\Users\barte\Desktop/sin.txt', 'w') as fp:
    for item in SIN:
         #write each item on a new line
        fp.write("%s, " % item)
    print('Saving sin values to file Done')
    


'''   
# DATA FROM A FILE
my_file, fs = sf.read('speech0001.wav')
my_file = my_file[3000::40]

# convertion
final_data = []

for i in my_file:
    if abs(int(400*i))==1:
        final_data.append(abs(int(400*i))-1)
    elif abs(int(400*i))==2:
        final_data.append(abs(int(400*i))-2)
    elif abs(int(400*i))==10:
        final_data.append(abs(int(400*i))+1)
    else:
        final_data.append(abs(int(400*i)))


# GIVEN DATA
wave1 = [   
113, 84, 136, 173, 132, 143, 150, 100, 126, 113, 94, 153, 148, 122, 172, 131, 91, 132, 88, 102, 124, 130, 167,
129, 112, 149, 142, 105, 119, 132, 142, 118, 114, 133, 145, 152, 91, 97, 133, 136, 116, 103, 119, 123, 116, 155,
154, 110, 135, 125, 109, 136, 97, 97, 148, 126, 169, 161, 76, 123, 163, 112, 116, 133, 140, 172, 131, 117, 136,
136, 115, 105, 154, 137, 109, 173, 174, 114, 112, 95, 127, 168, 119, 68, 132, 206, 115, 87, 136, 149, 109, 71,
151, 171, 97, 100, 168, 172, 136, 91, 113, 166, 130, 90, 115, 122, 129, 148, 114, 111, 141, 126, 111, 120, 123,
138, 136, 157, 138, 109, 130, 115, 106, 128, 133, 115, 113, 107, 165, 180, 75, 90, 166, 146, 83, 89, 136, 175,
147, 72, 123, 148, 122, 101, 115, 144, 141, 116, 121, 164, 144, 100, 108, 131, 144, 138, 101, 153, 177, 135, 120,
123, 121, 93, 100, 178, 142, 87, 147, 171, 130, 94, 130, 137, 137, 103, 117, 148, 127, 139, 135, 108, 129, 133,
117, 127, 119, 96, 130, 151, 123, 118, 111, 143, 134, 106, 100, 163, 121, 81, 172, 204, 119, 82, 123, 150, 138,
85, 112, 175, 187, 102, 110, 151, 133, 98, 86, 135, 159, 134, 126, 132, 112, 110, 112, 104, 138, 144, 115, 136,
145, 128, 130, 132, 82, 88, 187, 189, 76, 92, 187, 190, 93, 79, 149, 163, 115, 74, 127, 153, 125, 116, 131, 163,
152, 100, 98, 136, 140, 91, 115, 178, 144, 134, 119, 118, 148, 117, 131, 83, 76, 211, 200, 56, 76, 164, 143, 96,
77, 124, 186, 157, 83, 118, 146, 122, 92, 112, 151, 155, 107, 94, 147, 131, 111, 109, 154, 138, 98, 133, 143, 111,
148, 151, 68, 116, 214, 143, 39, 129, 168, 142, 133, 94, 142, 197, 116, 78, 141, 129, 132, 110, 133, 193, 165, 97,
100, 128, 120, 98, 95, 131, 171, 141, 102, 162, 120, 144, 104, 37, 189, 215, 70, 87, 183, 157, 132, 85, 90, 169,
173, 90, 98, 152, 147, 116, 93, 131, 163, 124, 83, 121, 138, 125, 126, 128, 157, 144, 108, 111, 131, 146, 108, 60,
139, 235, 153, 56, 117, 172, 131, 104, 81, 126, 198, 148, 82, 117, 154, 116, 75, 106, 183, 145, 103, 108, 150,
132, 100, 98, 117, 153, 123, 140, 140, 159, 111, 60, 152, 204, 108, 74, 142, 160, 147, 103, 90, 156, 180, 120, 97,
118, 147, 130, 94, 119, 168, 158, 139, 100, 122, 129, 95, 116, 119, 161, 144, 118, 158, 146, 63, 51, 155, 191,
101, 98, 170, 178, 144, 71, 80, 159, 150, 96, 111, 144, 165, 130, 91, 117, 151, 153, 105, 106, 140, 138, 107, 107,
98, 177, 144, 86, 169, 59, 78, 214, 122, 61, 171, 171, 154, 155, 63, 100, 184, 120, 86, 148, 164, 173, 122, 85,
119, 112, 103, 131, 127, 135, 161, 137, 112, 109, 127, 141, 140, 90, 92, 197, 172, 59, 115, 148, 139, 174, 90,
102, 188, 126, 94, 130, 131, 141, 120, 111, 125, 128, 117, 96, 123, 142, 158, 136, 109, 139, 131, 86, 148, 124,
41, 154, 234, 113, 58, 135, 136, 164, 125, 53, 159, 209, 131, 99, 96, 136, 151, 96, 101, 119, 137, 156, 115, 104,
126, 117, 150, 129, 118, 175, 155, 82, 68, 183, 200, 90, 75, 140, 173, 158, 81, 63, 179, 203, 127, 100, 124, 174,
141, 86, 98, 148, 155, 132, 117, 126, 149, 97, 97, 127, 152, 135, 140, 86, 91, 217, 115, 30, 118, 147, 162, 145,
59, 110, 206, 145, 60, 106, 149, 159, 143, 92, 110, 154, 135, 124, 96, 115, 166, 137, 97, 103, 142, 160, 134, 52,
114, 225, 146, 57, 91, 133, 166, 152, 75, 129, 209, 130, 79, 104, 124, 159, 120, 98, 168, 178, 127, 77, 104, 165,
117, 87, 136, 160, 151, 140, 77, 58, 185, 190, 69, 106, 172, 174, 166, 97, 79, 187, 177, 87, 118, 140, 149, 133,
88, 109, 157, 154, 99, 102, 155, 131, 94, 87, 130, 169, 147, 138, 66, 91, 211, 131, 25, 111, 170, 167, 155, 94,
103, 168, 130, 84, 98, 133, 162, 132, 114, 120, 140, 115, 79, 122, 142, 142, 123, 127, 176, 140, 114, 56, 76, 230,
163, 47, 109, 158, 174, 149, 73, 103, 201, 189, 85, 72, 133, 165, 134, 84, 132, 175, 134, 111, 94, 107, 140, 124,
131, 146, 148, 184, 153, 43, 72, 196, 157, 58, 117, 161, 183, 179, 51, 64, 184, 148, 87, 106, 147, 186, 131, 75,
128, 144, 113, 100, 107, 163, 136, 93, 114, 145, 150, 139, 96, 52, 187, 208, 46, 67, 148, 155, 191, 115, 45, 176,
184, 73, 69, 116, 177, 159, 103, 142, 160, 122, 102, 66, 133, 172, 111, 112, 167, 158, 118, 128, 65, 63, 194, 176,
80, 124, 132, 163, 168, 60, 71, 181, 182, 124, 99, 127, 171, 144, 108, 85, 163, 176, 103, 112, 128, 152, 130, 107,
146, 144, 153, 138, 35, 89, 214, 130, 50, 117, 174, 205, 154, 52, 95, 172, 143, 85, 93, 162, 201, 126, 65, 119,
141, 112, 69, 109, 193, 149, 99, 131, 129, 144, 98, 15, 135, 239, 131, 58, 110, 169, 192, 107, 41, 129, 210, 169]


# EXAMPLE SIN CONTROL
example_control = [3, 0, 34, 5, 6, 8, 9, 89, 90, 123]


#  to  bytes
b_wave1 = bytes(wave1)
#b_my_file = bytes(final_data)
b_control = bytes(example_control)


ser = Serial("COM3", 28800)
play_sin = b'\x02\x01\x31\x0a'   # send   1
play_sig = b'\x02\x01\x32\x0a'   # send   2

## Byte values
#print(b_my_file)
#print(b_wave1)

# RESPONSE FROM SOURCE
ser.write(b'\x0c')
print("Checking connection ... ")
ser.write(b'\x0c')
while(True):
    ser.write(b'\x0c')
    check = ser.read(16)
    if check[0] : print("   Received something")
    ser.write(b'\x0c')
    if check.decode() == "Connection works":
        print("   " + check.decode() + " ")
        break
    ser.write(b'\x0c')




while (True):
    choice = input(" Select to send signal data signal or  give some command ")
    
    if choice == "play sin":
        ser.write(play_sin)
        
    ##elif choice == "my sig":
        #ser.write(b'\x01')
        #ser.write(b_my_file)
        #ser.write(b'\x0a')
        
    elif choice == "wave":
        ser.write(b'\x01')
        ser.write(b_wave1)
        ser.write(b'\x0a')

    elif choice == "example":
        ser.write(b'\x01')
        ser.write(b_control)
        ser.write(b'\x0a')

    elif choice == "play sig":
        ser.write(play_sig)
        
    else:
        print(" Wrong command ")
        

'''




    
