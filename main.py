import gc
import speech_model_library as model
from machine import I2S, PWM, Pin, reset
from time import sleep
from machine import Timer


countdownflag=False
c=0
timer=Timer(0)
led=Pin(2,Pin.OUT)

def mic2init():         # initilazation of MIC (same mic diffrent init)
    global mic2
    sleep(0.5)
    mic2 = I2S(I2S.NUM0,ws=Pin(4), sdin=Pin(23), mode=I2S.MASTER_PDW,
            dataformat=I2S.B16, channelformat=I2S.ONLY_RIGHT,
            samplerate=16000, dmacount=16, dmalen=256)
    
def mic1init():         # initilazation of MIC(same mic diffrent init)
    global mic1
    sleep(0.5)
    mic1 = I2S(I2S.NUM0,ws=Pin(4), sdin=Pin(23), mode=I2S.MASTER_PDW,
        dataformat=I2S.B16, channelformat=I2S.ONLY_RIGHT,
        samplerate=16000, dmacount=16, dmalen=256)
    
buffer = bytearray(8192)    # buffer for mic data
label = '' 
gc.collect()

mic1init() 

def countdown(Pin):   # Timer for 8 seconds
    global c,countdownflag
    c+=1
    if(c==8):
        print("TimesUp, Back to WAKEUP mode")
        timer.deinit()
        mic2.deinit()
        mic1init()
        countdownflag=True
        
def task():             # Command listining mode
    global countdownflag
    mic1.deinit()       # Deinit Mic
    mic2init()          # init mic
    led.on()            
    timer.init(period=1000, mode=Timer.PERIODIC, callback=countdown)        #Timer init
    while countdownflag!=True:
        global l1,prob1    
        mic2.readinto(buffer)               # reading mic data into buffer
        l1, prob1 = model.predict(buffer)
        print("listining...")
        gc.collect()
        if(l1=="LightOn"):       # if speech command is "LIGHT ON" 
            print("command is LIGHT ON")
            timer.deinit()
            mic2.deinit()
            break

        #if(l1=="LightOff"):
        elif(l1=="LightOff"):        # if speech command is "LIGHT OFF"
            print("command is LIGHT OFF")
            timer.deinit()
            mic2.deinit()
            break
    mic2.deinit()
    countdownflag=False
            
while True:         # WAKE UP command listining mode
    print("say ' RIGHT ' as WAKEUP command!")
    mic1.readinto(buffer)
    l, prob = model.predict(buffer)
    gc.collect()
    if l == '[OTHER]' or prob <= 70:
        continue
    label = l
    model.snapshot()
    if l == 'Right':        
        print(" WAKEUP ")
        mic1.deinit()
        task()          # Goes to COMMAND listining mode for 8 seconds
        led.off()
        mic1init()  
        
    

