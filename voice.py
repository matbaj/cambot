import subprocess
import speech_recognition as sr
import threading
import re


class VoiceResponse:
	def say(self, text):
		p = re.compile(ur'\.')
		subst = u"<break time='1s'/>"
		result = re.sub(p, subst, text)
		cmd = "espeak -m  \"%s\"" %(result)
		subprocess.call(cmd, shell=True)

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
	    print "DEBUG: RECOGNISED: %s" % r
	    self.callback(r)	
        except LookupError:
            print "Recognision Error" 
            return(-1)


