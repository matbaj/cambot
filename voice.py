import subprocess

class VoiceResponse:
	def say(self, text):
		subprocess.call("espeak \"%s\"" %(text), shell=True)



