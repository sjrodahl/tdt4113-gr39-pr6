from PIL import Image
from basic_robot.basic_robot.camera import Camera

class RedandBLue():

    def __init__(self):
        #self.image = Image.open("redandblue.jpg")
        self.image = Camera.get_value()

    def get_pixel(self,x,y):
        return self.image.getpixel((x,y))

    def put_pixel(self,x,y,):
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

        self.image.show()


    def Array(self):
        self.Content = []

        for x in range(self.image.size[0]):
            temp = [0,0]
            for y in range(self.image.size[1]):
                temp[0] += self.get_pixel(x,y)[0]
                temp[1] += self.get_pixel(x,y)[2]

            if (temp[0] > 2000) or (temp[1] > 2000):
                if(temp[0] > temp[1]):
                    self.Content.append("Red")
                else:
                    self.Content.append("Blue")
            else:
                self.Content.append(None)

        print(self.Content)

Hallvard = RedandBLue()
Hallvard.Converter()
Hallvard.Array()