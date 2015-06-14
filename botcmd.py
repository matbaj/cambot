import cmd
import code

class BotCMD(cmd.Cmd):
    """Command line for bot"""

    prompt = "[BOT] >> "
    voice_response=0
    voice_recogniser=0

    def do_say(self, line):
        voice.say(line)

    def do_set_voice(self,line):
        self.voice_response=int(line)

    def do_set_recogniser(self,line):
	if int(line) == 0:
		print "KNOWN BUG: You need to do last request to kill listener"
		self.voice_recogniser=0
		recogniser.stop()
	else:
		self.voice_recogniser=1
		recogniser.start()

    def do_order(self,line):
        """Order command to ai"""
        reps = AI.act(line)
        for r in reps:
            print r
            if self.voice_response != 0:
                voice.say(r)

    def do_init(self,line):
        """Initialize devices"""
        print "Initialization Done"

    def do_inter(self, line):
        """Drop to interpreter"""
        code.interact(local=locals())
    
    def do_EOF(self, line):
        return self.quit()
    def do_quit(self,line):
        """Quiting application"""
        return self.quit()

    def quit(self):
	if self.voice_recogniser == 1:
		self.do_set_recogniser(0)
	return True

    def process_voice(self,text):
	if self.voice_recogniser == 1:  #in case if we turn off voice recognision and it still listen
		self.do_order(text)

    def emptyline(self):
        """Do not repeat last line"""
        pass

    def default(self, line):
        self.do_order(line)
