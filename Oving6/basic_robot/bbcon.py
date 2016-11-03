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



class BBCON:
    def __init__(self):
        self.behaviors = []         # all behaviors
        self.active = []            # active behaviors
        self.inactive = []          # inactive behaviors
        
        self.sensobs = []           # sensor objects
        self.motobs = []            # motor object(s)
        self.arbitrator = None      # tar inn recommendation og gjør om til motor request
        self.timestamp = 0
        
    def add_behavior(self,b):
        self.behaviors.append(b)
    
    def add_sensob(self,s):
        self.sensobs.append(s)
    
    def activate(self,b):
        if b in self.inactive_behaviors:
            self.active.append(b)
            self.inactive.remove(b)
    
    def deactivate(self,b):
        if b in self.active_behaviors:
            self.inactive.append(b)
            self.active.remove(b)
            
    def run():
        pass