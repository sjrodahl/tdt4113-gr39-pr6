from PIL import Image
from camera import Camera
from ultrasonic import Ultrasonic
from irproximity_sensor import IRProximitySensor
from reflectance_sensors import ReflectanceSensors

class Sensob():

    

    def __init__(self, bbcon):
        self.bbcon = bbcon
        self.bbcon.add_sensob(self)
        self.behaviors = []
        #self.update()

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)

    def any_active_behaviors(self):
        #for b in self.behaviors:
        #    print(str(b) + str(b.active_flag))
        if len(self.behaviors) == 0:
            return False
        t = [b.active_flag for b in self.behaviors]
        #print(t)
        #print(any(t))
        return any([b.active_flag for b in self.behaviors])

    def update(self):
        pass

    def reset(self):
        pass

    def get_value(self):
        pass


class RedandBlueSensob(Sensob):
    camera = Camera()
    image = None
    #image = Image.open("redandblue.jpg")

    content = []
    def get_pixel(self,x,y):
        return self.image.getpixel((x,y))

    def put_pixel(self,x,y):
        Black = (0, 0, 0)
        return self.image.putpixel((x,y),Black)

    def Converter(self):

        for x in range(self.image.size[0]):
            for y in range(self.image.size[1]):
                #print((self.get_pixel(x,y))[1:])
                # placing between 0 and 80 so that red with some small variationes are not removed
                if (self.get_pixel(x,y)[1] >=(0)) and (self.get_pixel(x,y)[1] <=(80)):
                    pass
                else:
                    self.put_pixel(x,y)

                    #self.image.show()

    def Array(self):

        for x in range(self.image.size[0]):
            temp = [0,0]
            for y in range(self.image.size[1]):
                temp[0] += self.get_pixel(x,y)[0]
                temp[1] += self.get_pixel(x,y)[2]

            if (temp[0] > 500) or (temp[1] > 500):
                if(temp[0] > temp[1]):
                    self.content.append("Red")
                else:
                    self.content.append("Blue")
            else:
                self.content.append(None)

                #print(self.content)

    def update(self):
        if not self.any_active_behaviors():
            return 0
        print("Camera updated")
        self.image = self.camera.update()
        self.Converter()
        self.Array()
        return self.content

    def reset(self):
        self.camera.reset()

    def get_value(self):
        return self.content


class UltrasonicSensob(Sensob):
    ultra = Ultrasonic()
    distance = 1

    def update(self):
        if not self.any_active_behaviors():
            return 0
        print("Ultra updated")
        self.ultra.update()
        self.distance = self.ultra.get_value()
    
    def any_active_behaviors(self):
        return True

    def reset(self):
        self.ultra.reset()

    def get_value(self):
        return self.distance


class IrSensob(Sensob):
    ir = IRProximitySensor()
    is_close = [False, False]

    def update(self):
        if not self.any_active_behaviors():
            return 0
        print("IR updated")
        self.is_close = self.ir.update()

    def reset(self):
        self.ir.reset()

    def get_value(self):
        return self.is_close


class ReflectanceSensob(Sensob):

    reflector = ReflectanceSensors(min_reading=150, max_reading=1000, auto_calibrate=False)
    reflectance_array = [False] * 6


    def update(self):
        print("reflectance updated")
        if not self.any_active_behaviors():
            return 0
        self.reflectance_array = self.reflector.update()
        #print(self.reflectance_array)
        self.find_line()

    def find_line(self):
        array = [(x<0.5) for x in self.reflectance_array]
        self.reflectance_array = array

    def reset(self):
        self.reflectance_array = [False] * 6

    def get_value(self):
        return self.reflectance_array
