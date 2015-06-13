#!/usr/bin/env python2
from bot import *
from voice import *

import __builtin__

__builtin__.VoiceResponse = VoiceResponse

if __name__ == '__main__':
    BotCMD().cmdloop()
