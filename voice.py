import subprocess
import speech_recognition as sr
import threading

class VoiceResponse:
	def say(self, text):
		subprocess.call("espeak -g 3  \"%s\"" %(text), shell=True)

class VoiceRecogniser(threading.Thread):
    def __init__(self,callback,lang="en-US"):
	super(VoiceRecogniser, self).__init__()
        self.recogniser = sr.Recognizer(language=lang)
        self.running =True
	self.source = sr.Microphone()
	self.callback= callback

    def run(self):
	print "Recogniser started"
	while self.running:
		with self.source as s: audio = self.recogniser.listen(s)		
		self.process(audio)
	print "Recogniser stopped"
    def stop(self):
        self.running=False        

    def process(self, audio):
        try:
            r = self.recogniser.recognize(audio)
	    self.callback(r)	
        except LookupError:
            print "Recognision Error" 
            return(-1)


