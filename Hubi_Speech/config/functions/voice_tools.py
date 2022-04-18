import speech_recognition as sr
import os
from gtts import gTTS

#Define the microphone function to record the user's voice and return the recognized speech
microphone = sr.Microphone()
recognition_listen = sr.Recognizer().listen
recognition_results = sr.Recognizer().recognize_google

#Google Speech to Text
def speak(text):
    tts = gTTS(text=text, lang='es')
    filename = 'config/functions/__pycache__/record.mp3'
    tts.save(filename)
    os.system(f'afplay {filename}')
    #Remove temp audio file
    os.remove(filename)