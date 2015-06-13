import subprocess
import speech_recognition as sr

class VoiceResponse:
	def say(self, text):
		subprocess.call("espeak \"%s\"" %(text), shell=True)

class VoiceRecogniser:
    def __init__(lang="pl"):
        self.recorder = sr.Recognizer(language=lang)
        self.thread = None

    def start(self):
        self.thread = self.recorder.listen_in_background(sr.Microphone(), self.callback)

    def stop(self):
        

    def callback(self,recognizer, audio):                          # this is called from the background thread
        try:
            return(recognizer.recognize(audio))  # received audio data, now need to recognize it
        except LookupError:
            print "Recognision Error" 
            return(-1)

