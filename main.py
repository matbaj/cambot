#!/usr/bin/env python2
from botcmd import *
from voice import *

import __builtin__

__builtin__.VoiceResponse = VoiceResponse
__builtin__.AI = AIController(0,0)

if __name__ == '__main__':
    BotCMD().cmdloop()
