import cmd

class BotCMD(cmd.Cmd):
    """Command line for bot"""

    prompt = "[BOT] >> "


    def do_greet(self, line):
        print "hello"

    def do_init(self,line):
        """Initialize devices"""
        print "Initialization Done"
    
    def do_EOF(self, line):
        return True
    def do_quit(self,line):
        """Quiting application"""
        return True
