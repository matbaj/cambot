import cmd
import code

class BotCMD(cmd.Cmd):
    """Command line for bot"""

    prompt = "[BOT] >> "


    def do_greet(self, line):
        print "hello"

    def do_order(self,line):
        """Order command to ai"""
        reps = AI.act(line)
        for r in reps:
            print r

    def do_init(self,line):
        """Initialize devices"""
        print "Initialization Done"

    def do_inter(self, line):
        """Drop to interpreter"""
        code.interact(local=locals())
    
    def do_EOF(self, line):
        return True
    def do_quit(self,line):
        """Quiting application"""
        return True

    def emptyline(self):
        """Do not repeat last line"""
        pass

    def default(self, line):
        self.do_order(line)