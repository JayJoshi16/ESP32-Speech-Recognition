import gc
import speech_model_wake as wake
from machine import I2S, PWM, Pin, reset
from time import sleep
from machine import Timer


#   ws_pin = Pin(15)   # Word clock output
#   sdin_pin = Pin(13) # Serial data input

countdownflag=False
c=0
timer=Timer(0)
led=Pin(2,Pin.OUT)
def mic2init():
    global mic2
    sleep(0.5)
    mic2 = I2S(I2S.NUM0,ws=Pin(4), sdin=Pin(23), mode=I2S.MASTER_PDW,
            dataformat=I2S.B16, channelformat=I2S.ONLY_RIGHT,
            samplerate=16000, dmacount=16, dmalen=256)
    
def mic1init():
    global mic1
    sleep(0.5)
    mic1 = I2S(I2S.NUM0,ws=Pin(4), sdin=Pin(23), mode=I2S.MASTER_PDW,
        dataformat=I2S.B16, channelformat=I2S.ONLY_RIGHT,
        samplerate=16000, dmacount=16, dmalen=256)
    
buffer = bytearray(8192)
label = ''
gc.collect()

mic1init()

def countdown(Pin):
    global c,countdownflag
    c+=1
    if(c==8):
        print("TimesUp, Back to WAKEUP mode")
        timer.deinit()
        mic2.deinit()
        mic1init()
        countdownflag=True
        
def task():
    global countdownflag
    mic1.deinit()
    mic2init()
    led.on()
    timer.init(period=1000, mode=Timer.PERIODIC, callback=countdown)
    while countdownflag!=True:
        global l1,prob1    
        mic2.readinto(buffer)
        l1, prob1 = wake.predict(buffer)
        print("listining")
        gc.collect()
        if(l1=="LightOn"):
            print("on")
            timer.deinit()
            mic2.deinit()
            break
        if(l1=="LightOff"):
            print("off")
            timer.deinit()
            mic2.deinit()
            break
    mic2.deinit()
    countdownflag=False
            
while True:
    print("say 'RIGHT' !")
    mic1.readinto(buffer)
    l, prob = wake.predict(buffer)
    gc.collect()
    if l == '[OTHER]' or prob <= 70:
        continue
    label = l
    wake.snapshot()
    if l == 'Right': 
        print("WAKEUP")
        mic1.deinit()
        task()
        led.off()
        mic1init()  
        
    

