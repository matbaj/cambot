import speech_recognition as sr
from os import system
r = sr.Recognizer()
with sr.Microphone() as source:                # use the default microphone as the audio source
    audio = r.listen(source)                   # listen for the first phrase and extract it into audio data

try:
    text = r.recognize(audio)
    print("You said "+ text)    # recognize speech using Google Speech Recognition
    system("espeak '%s' " % (text))
except LookupError:                            # speech is unintelligible
    print("Could not understand audio")
