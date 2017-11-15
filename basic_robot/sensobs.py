from PIL import Image
from camera import Camera
from ultrasonic import Ultrasonic
from irproximity_sensor import IRProximitySensor
from reflectance_sensors import ReflectanceSensors

class Sensob():

    def __init__(self, bbcon):
        self.bbcon = bbcon
        self.bbcon.add_sensob(self)


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
        self.content = []

        for x in range(self.image.size[0]):
            temp = [0,0]
            for y in range(self.image.size[1]):
                temp[0] += self.get_pixel(x,y)[0]
                temp[1] += self.get_pixel(x,y)[2]

            if (temp[0] > 2000) or (temp[1] > 2000):
                if(temp[0] > temp[1]):
                    self.content.append("Red")
                else:
                    self.content.append("Blue")
            else:
                self.content.append(None)

                #print(self.content)

    def update(self):
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
        self.ultra.update()
        self.distance = self.ultra.get_value()

    def reset(self):
        self.ultra.reset()

    def get_value(self):
        return self.distance


class IrSensob(Sensob):
    ir = IRProximitySensor()
    is_close = [False, False]

    def update(self):
        self.is_close = self.ir.update()

    def reset(self):
        self.ir.reset()

    def get_value(self):
        return self.is_close


class ReflectanceSensob(Sensob):

    reflector = ReflectanceSensors(min_reading=150, max_reading=1800)
    reflectance_array = [False] * 6


    def update(self):
        self.reflectance_array = self.reflector.update()
        print(self.reflectance_array)
        self.find_line()

    def find_line(self):
        array = [(x<0.5) for x in self.reflectance_array]
        self.reflectance_array = array

    def reset(self):
        self.reflectance_array = [False] * 6

    def get_value(self):
        return self.reflectance_array
