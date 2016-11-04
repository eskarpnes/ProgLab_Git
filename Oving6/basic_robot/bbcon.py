from zumo_button import ZumoButton as btn
from motors import Motors as motor
from reflectance_sensors import ReflectanceSensors as scanner

button = btn()
m = motor()
def main():
    button.wait_for_press()
    m.forward(speed=0.5, dur=0.5)
    m.backward(speed=0.5, dur=0.5)    

main()

class MotorObj:
    def __init__(self):
        # definer funksjoner for alle sensorene i en dict
        self.sensors = {
            Camera:             self.react_camera,
            IRProximitySensor:  self.react_IR,
            ReflectanceSensors: self.react_reflect,
            Ultrasonic:         self.react_ultra
        }
        self.current_value = 0
        
    def run(sensor, value):
        # tar inn en tuppel med sensor, verdi
        '''
        feks:
        kamera ser at et objekt dekker nesten hele field-of-view (objektet er nært)
        får da inn en høy verdi i tuppelen, og må feks rygge lengre bak, enn om objektet hadde vært lengre unna
        '''
        sensor = sensor.__class__.__name__
        print ('Motor controller received the highest priority from',sensor,'with a value of',value)
        
        # ...finnes sensoren?
        if sensor in self.sensors:
            # kjører funksjonen definert i self.sensors-dict
            self.sensors[name]()
            current_value = value
        
    # definer hvordan motoren skal reagere for hver type sensor - bruk self.current_value
    def react_camera(self):
        pass
        
    def react_IR(self):
        pass
        
    def react_reflect(self):
        pass
        
    def react_ultra(self):
        pass

class Arbitrator:
    def __init__(self):
        self.current_motor_rec = None
        self.motor = MotorObj()
        
    def choose_action(self, sensors):
        # hent ut den høyst prioriterte sensoren ut fra lista
        # og lag så en "motor recommendation"
        sensor_type,value = max(sensors, key=itemgetter(1))
        self.motor.run(sensor_type,value)
        self.wait()
        
    def wait(self):
        # implementer threading?
        pass

class BBCON:
    def __init__(self):
        self.ARB = Arbitrator()
    
        self.behaviors = []         # all behaviors
        self.active = []            # active behaviors
        self.inactive = []          # inactive behaviors
        
        self.sensobs = []           # sensor objects
        self.motobs = []            # motor object(s), useless?!?!

        self.timestamp = 0
        self.motor_runtime = 0.5
        
    def add_behavior(self,b):
        self.behaviors.append(b)
    
    def add_sensob(self,s):
        self.sensobs.append(s)
    
    def activate(self,b):
        if b in self.inactive_behaviors and b in self.behaviors:
            self.active.append(b)
            self.inactive.remove(b)
    
    def deactivate(self,b):
        if b in self.active_behaviors and b in self.behaviors:
            self.inactive.append(b)
            self.active.remove(b)
            
    def run(self):
        current_data = []
        for sensor in self.sensobs:
            current_data.append(sensor, sensor.update()) # returnerer kun verdi
            # oppdaterer current_data med prioritet og verdi til enhver sensor
            # denne skal være en tuppel med (sensortype, verdi)
        self.ARB.choose_action(current_data)
        self.reset()
    
    def reset(self):
        self.timestamp += 1
        for sensor in self.sensobs:
            sensor.reset()