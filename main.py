#!/usr/bin/env python2
from botcmd import *
from voice import *
from aicontroller import *
from camera import *

import __builtin__

__builtin__.VoiceResponse = VoiceResponse
__builtin__.AI = AIController()
__builtin__.voice = VoiceResponse()
__builtin__.camera = Camera()

if __name__ == '__main__':
    BotCMD().cmdloop()
