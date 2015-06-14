#!/usr/bin/env python2
from botcmd import *
from voice import *
from aicontroller import *
from camera import *

import __builtin__

botcmd = BotCMD()
__builtin__.VoiceResponse = VoiceResponse
__builtin__.AI = AIController()
__builtin__.voice = VoiceResponse()
__builtin__.camera = Camera()
__builtin__.recogniser = VoiceRecogniser(botcmd.process_voice)

if __name__ == '__main__':
    try:
        config = open('%s.conf' % sys.argv[1]) 
    except IndexError:
        config = open('default.conf')
    for cmd in config.readlines():
        if not cmd.startswith('#'):
            botcmd.onecmd(cmd)
    print "Confing loaded dropping to shell"
    botcmd.cmdloop()
