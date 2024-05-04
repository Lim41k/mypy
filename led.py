import time
import sys

LEDs=4
LEDPATH='/sys/class/leds/beaglebone:green:usr'

f = []
for i in range(LEDs):
    f.append(open(LEDPATH+str(i)+"/brightness", "w"))

# init -> write 0 to use leds
for i in range(LEDs):
   f[i].seek(0)
   f[i].write("0")



while True:

    print("choose led")
    s = input()
   
    if s == "1":
        f[i].seek(0)
        f[0].write("1")
        time.sleep(2)
        f[0].write("0")
        print("ok")
    elif s ==  "2":
        f[i].seek(0)
        f[1].write("1")
        time.sleep(2)
        f[1].write("0")
        print("ok")
    elif s ==  "3":
        f[i].seek(0)
        f[2].write("1")
        time.sleep(2)
        f[2].write("0")
        print("ok")
    elif s ==  "4":
        f[i].seek(0)
        f[3].write("1")
        time.sleep(2)
        f[3].write("0")
        print("ok")
    else :
        sys.exit("Bue")