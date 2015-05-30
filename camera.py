class Camera:
    def __init__():
        self.camera_x = 60
        self.camera_y = 80
        set_x(camera_x)
        set_y(camera_y)

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


