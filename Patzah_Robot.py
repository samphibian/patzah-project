from Adafruit_PWM_Servo_Driver import PWM
import atexit
import grove_i2c_temp_hum_mini
import grovepi
from grove_rgb_lcd import *
import time

pwm = PWM(0x40)
pwm.setPWMFreq(60)                        # Set frequency to 60 Hz

servoMin = 150

class Robot():
    def __init__(self, configFileName = "DoNotNameYourConfigFileThisOrYouWillNeedToManuallyEnterThePorts"):
        self.dct = {}
        self.dct["analogInput"] = {}
        self.dct["analogOutput"] = {}
        self.dct["digitalInput"] = {}
        self.dct["digitalOutput"] = {}
        self.dct["servos"] = {}
        
        if (configFileName == "DoNotNameYourConfigFileThisOrYouWillNeedToManuallyEnterThePorts"):
            anaIn = []
            anaOut = []
            digIn = []
            digOut = []
            servs = []
            ai = int(input("How many analog sensors do you have? "))
            for i in range(ai):
                a = input("Please enter a sensor name ")
                print("In what A# port is ", a, "? (Please only type the #)")
                self.dct["analogInput"][a] = int(input ())
                grovepi.pinMode(self.dct["analogInput"][a], "INPUT")
            ao = int(input("How many analog outputs do you have? "))
            for i in range(ao):
                a = input("Please enter a sensor name ")
                print("In what A# port is ", a, "? (Please only type the #)")
                self.dct["analogOutput"][a] = int(input ())
                grovepi.pinMode(self.dct["analogOutput"][a], "OUTPUT")
            di = int(input("How many digital sensors do you have? "))
            for i in range(di):
                d = input("Please enter a sensor name ")
                print("In what D# port is ", d, "? (Please only type the #)")
                self.dct["digitalInput"][d] = int(input ())
                grovepi.pinMode(self.dct["digitalInput"][d], "INPUT")
            do = int(input("How many digital outputs do you have? "))
            for i in range(do):
                d = input("Please enter a sensor name ")
                print("In what D# port is ", d, "? (Please only type the #)")
                self.dct["digitalOutput"][d] = int(input ())
                grovepi.pinMode(self.dct["digitalOutput"][d], "OUTPUT")  
            sr = int(input("How many servos do you have? "))
            for i in range(sr):
                s = input("Please enter a sensor name ")
                print("In what channel is ", s, "? (Please only type the #)")
                self.dct["servos"][s] = int(input ())  
        else:        
            f = open(configFileName, 'r')
            for line in f:
                vals = line.split(", ")
                count = 0
                name = vals[0]
                if vals[0]+str(count) in self.dct[vals[1]]:
                    while(self.dct[vals[1]][vals[0]+str(count)]):
                        count += 1
                self.dct[vals[1]][name + str(int(vals[2]))] = int(vals[2])  
        print(self.dct)
        
    def end(self):
        snsrs = self.dct
        for x in snsrs["digitalOutput"]:
            self.writeOutput(x, 0)
        for x in snsrs["analogOutput"]:
            self.writeOutput(x, 0)
        for s in snsrs["servos"]:
            self.moveServo(s, servoMin)
        print("Goodbye")
        
    def readInput(self, snsr):
        ai = self.dct["analogInput"]
        di = self.dct["digitalInput"]
        if snsr in ai:
            return grovepi.analogRead(ai[snsr])
        elif snsr in di:
            return grovepi.digitalRead(di[snsr]) 
        else:
            print ("Sensor ", snsr, " not found; would you like to add it? (y, n)")
            r = input()
            if r == 'y':
                self.addPort(snsr, "INPUT")
                self.readInput(snsr)
                    
    def writeOutput(self, snsr, val):
        aout = self.dct["analogOutput"]
        dout = self.dct["digitalOutput"]
        if snsr in aout:
            return grovepi.analogWrite(aout[snsr], val)
        elif snsr in dout:
            return grovepi.digitalWrite(dout[snsr], val) 
        else:
            print ("Sensor ", snsr, " not found; would you like to add it? (y, n)")
            r = input()
            if r == 'y':
                self.addPort(snsr, "OUTPUT")
                self.writeOutput(snsr, val)
                
    def moveServo(self, servo, val):
        s = self.dct["servos"]
        if servo in s:
            pwm.setPWM(s[servo], 0, val)    
        else:
            print ("Servo ", servo, " not found; would you like to add it? (y, n)")
            r = input()
            if r == 'y':
                c = ("Please enter the channel of the servo")
                s[servo] = c
                    
    def addPort(self, snsr, io):
        port = input("Please input the port, eg a0 or d5 ")
        if port[0] == 'a' and 0 <= int(port[1]) and 2 >= int(port[1]):
            if io == "OUTPUT": aio = self.dct["analogOutput"] 
            else: aio = self.dct["analogInput"]
            aio[snsr] = int(port[1])
            grovepi.pinMode(aio[snsr], io)
        elif port[0] == 'd' and 0 <= int(port[1]) and 8 >= int(port[1]):
            if io == "OUTPUT": dio = self.dct["digitalOutput"] 
            else: dio = self.dct["digitalInput"]
            dio[snsr] = int(port[1])
            grovepi.pinMode(dio[snsr], io)
        else:
            print ("Error reading input")
                    
    def convertLightToResistance(self, sensor_value):
        return (float)(1023 - int(sensor_value)) * 10 / int(sensor_value)
    
    def readEncoder(self):
        atexit.register(grovepi.encoder_dis)
        grovepi.encoder_en()
        return grovepi.encoderRead()
    
    def readTemp(self):
        t= grove_i2c_temp_hum_mini.th02()
        return t.getTemperature()
    
    def readHumidity(self):
        t= grove_i2c_temp_hum_mini.th02()
        return t.getHumidity()
    
    def display(self, color, txt):
        setText(txt)
        setRGB(color[0], color[1], color[2])