from os import system

class Camera:
    def __init__(self):
        self.camera_x = 60
        self.camera_y = 80
        self.set_x(self.camera_x)
        self.set_y(self.camera_y)
        self.face_tracking = 0

    #controling camera

    def set_x(self,val):
        self.camera_x = int(val)
        system("echo -en 'X%dZ' > /dev/ttyUSB0" % self.camera_x)

    def set_y(self,val):
        self.camera_y = int(val)
        system("echo -en 'Y%dZ' > /dev/ttyUSB0" % self.camera_y)

    def move_x(self,val):
        self.camera_x += int(val)
        self.set_x(self.camera_x)
    
    def move_y(self,val):
        self.camera_y += int(val)
        self.set_x(self.camera_y)

    def set_tracking(self,value):
        self.face_tracking = int(value)

    #TODO
    def show_no(self):
        pass
    
    def show_yes(self):
        pass
