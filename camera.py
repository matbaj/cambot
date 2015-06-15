from os import system
import cv2
import sys
import threading
servo_speed=2

#math part. You can skipt that

#freezone (When point is in this square then this is ok)
sh=100 #square height
sw=100 #square width

#640x480 camera resolution
w=640
h=480

#freezone x
sx = w/2-sw/2 #freezone field start
ex = w/2+sw/2 #freezone field stop

#freezone y
sy = h/2-sh/2 #freezone field start
ey = h/2+sh/2 #freezone field stop

class Camera(threading.Thread):
    def __init__(self):
	super(Camera, self).__init__()
        self.camera_x = 60
        self.camera_y = 80
        self.set_x(self.camera_x)
        self.set_y(self.camera_y)
        self.face_tracking = 1
	self.running = True

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

    def center_camera(self,x,y):
	if self.face_tracking ==1:
		if x<sx:
			if self.camera_x < 90:
				self.camera_x+=servo_speed
				self.set_x(self.camera_x)
		if x>ex:
			if self.camera_x > 30:
				self.camera_x-=servo_speed
				self.set_x(self.camera_x)
		if y<sy:
			if self.camera_y< 90:
				self.camera_y+=servo_speed/2
				self.set_y(self.camera_y)
		if y>ey:
			if self.camera_y > 30:
				self.camera_y-=servo_speed/2
				self.set_y(self.camera_y)
		

    def run(self):
	self.running=True
	print "Camera started"
	cascPath = "haarcascade_frontalface_default.xml"
	faceCascade = cv2.CascadeClassifier(cascPath)
	video_capture = cv2.VideoCapture(1)
	while self.running:
		#do stuff
		riet, frame = video_capture.read()
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = faceCascade.detectMultiScale(
		        gray,
		        scaleFactor=1.1,
		        minNeighbors=5,
		        minSize=(30, 30),
		        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		)
		for (x, y, w, h) in faces:
			X=x+w/2
			Y=y+h/2
			self.center_camera(X,Y)
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		cv2.imshow('Video', frame)
		cv2.waitKey(1)
	video_capture.release()
	cv2.destroyAllWindows()
	print "Camera stopped"

    def stop(self):
	self.running =False
