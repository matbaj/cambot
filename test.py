import cv2
import sys
from os import system
serwo_speed=2


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

    


def set_x(val):
    system("echo -en 'X%dZ' > /dev/ttyUSB0" % val)

def set_y(val):
    system("echo -en 'Y%dZ' > /dev/ttyUSB0" % val)

#free zone
ch=100
cw=100

w=640
h=480

ax = w/2-cw/2
ay = h/2-ch/2

bx = w/2+cw/2
by = h/2-ch/2

cx = w/2+cw/2
cy = h/2+ch/2

dx = w/2-cw/2
dy = h/2+ch/2


scx = 60
scy = 80

currentsx = scx

cascPath = sys.argv[1]
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(1)

while True:
    # Capture frame-by-frame
    riet, frame = video_capture.read()
    #height, width, depth = frame.shape
    #print "H:%d W:%d D:%d" % (height, width,depth)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        print "X: %d Y:%d" % (x,y)
        X=x+w/2
        Y=y+h/2
        if X<ax:
            print "lewo: %d" % (ax-X)
            if currentsx <90:
                currentsx+=serwo_speed
                set_x(currentsx)
                
        if X>bx:
            print "prawo: %d" % (X-bx) 
            if currentsx >30:
                currentsx-=serwo_speed
                set_x(currentsx)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
