from PIL import Image
from basic_robot.basic_robot.camera import Camera
from PIL import ImageColor
import math

class Value_measurer_blue():

    def __init__(self):
        self.image = Image.open("BLue.jpg")

        self.final = 0

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
                if (self.get_pixel(x,y)[:2] >=(0,0)) and (self.get_pixel(x,y)[:2] <=(80,80)):
                    pass
                else:
                    self.put_pixel(x,y)

        self.image.show()
    def Find_Placement(self):

        size = self.image.size[0]

        redvalueright = 0
        redvalueleft = 0


        if (size/2)%2 == 0:
            Split = size/2
        else:
            #litt feil margin her men tolererbart
            Split = int(round(size/2))

        for x in range(size):
            temp = 0
            if x <= Split:
                print("Left"+ str(x))

                for y in range(self.image.size[1]):
                    temp = (self.get_pixel(x,y)[2])
                    redvalueleft += temp

            else:
                print("Right" + str(x))
                for w in range(self.image.size[1]):
                    temp = self.get_pixel(x, w)[2]
                    redvalueright += temp

        if redvalueleft > redvalueright:

            self.direction = "Left"
            print("Left")

        else:
            self.direction = "Right"
            print("Right")



KK = Value_measurer_blue()
KK.Converter()
print (KK.Find_Placement())

class Value_measurer_red():



    def __init__(self):
        self.image = Image.open("Tester_red_center.jpg")

        self.image.show()
        self.final =0

    #def get_image(self):
        #self.image =Camera.update()

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
                if (self.get_pixel(x,y)[1:] >=(0,0)) and (self.get_pixel(x,y)[1:] <=(80,80)):
                    pass
                else:
                    self.put_pixel(x,y)

        self.image.show()

    def Find_Placement(self):

        size = self.image.size[0]

        redvalueright = 0
        redvalueleft = 0


        if (size/2)%2 == 0:
            Split = size/2
        else:
            #litt feil margin her men tolererbart
            Split = int(round(size/2))

        for x in range(size):
            temp = 0
            if x <= Split:
                print("Left"+ str(x))

                for y in range(self.image.size[1]):
                    temp = (self.get_pixel(x,y)[0])
                    redvalueleft += temp

            else:
                print("Right" + str(x))
                for w in range(self.image.size[1]):
                    temp = self.get_pixel(x, w)[0]
                    redvalueright += temp

        if redvalueleft > redvalueright:
                self.direction = "Left"

        else:
                self.direction = "Right"



    def Cool_stuff(self):
        size =self.image.size[0]

        redvalueright = []
        redvaluetotalright = 0
        redvalueleft = []
        redvaluetotalleft = 0



        if (size/2)%2 == 0:
           splitter = self.image.size[0]/2
           for x in range(size):
               temp = 0
               if x<=splitter:

                   for y in range(self.image.size[1]):

                       temp +=(self.get_pixel(x,y)[0])

                   redvalueright.append(temp)
                   redvaluetotalright +=temp
               else:
                   for y in range(self.image.size[1]):
                       temp +=(self.get_pixel(x, y)[0])
                   redvalueleft.append(temp)
                   redvaluetotalleft+= temp


        else:
            remover = int(round(self.image.size[0]/2))
            for x in range(size):
                temp = 0
                if x <= remover-1:

                    for y in range(self.image.size[1]):
                        temp+=(self.get_pixel(x, y)[0])
                    redvalueright.append(temp)
                    redvaluetotalright+=temp
                elif x == remover: pass
                else:
                    for y in range(self.image.size[1]):
                        temp +=(self.get_pixel(x, y)[0])
                    redvalueleft.append(temp)
                    redvaluetotalleft += temp

        map = []
        if redvaluetotalright > redvaluetotalleft:
            for q in range(len(redvalueright)):
                if redvalueright[q] != 0:
                    map.append(q)
        else:
            for q in range(len(redvalueleft)):
                print(q)
                if redvalueleft[q] != 0:
                    map[q].append(q)

        area =((round(len(map)*0.9))-(round(len(map)*0.1)))
        placement = [map[round(len(map)*0.1)], map[round(len(map)*0.9)]]

        print (area)
        print(placement)

        self.final =(placement[1]-(area/2))











"""k = Value_measurer()
k.Converter()
k.Find_Placement()
#k.Cool_stuff()"""