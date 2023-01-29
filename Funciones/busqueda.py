import sys
import speech_recognition
import pyttsx3 as tts


recognizer = speech_recognition.Recognizer()
voz = tts.init()
voz.setProperty('rate', 150)

def funcionEjemplo():
    global recognizer
    voz.say("hola como estas?")
    voz.runAndWait()

    terminar = False

    while not terminar:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                voz.say("ejemplo 1")
                voz.runAndWait()
                audio = recognizer.listen(mic)

                texto = recognizer.adjust_for_ambient_noise(audio)
                texto = texto.lower()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            voz.say("no entendi")
            voz.runAndWait()


def funcionejemplo2():
    global recognizer

    voz.say("ejemplo 2")
    voz.runAndWait()

    terminar = False

    while not terminar:
        try:
            with speech_recognition.Microphone() as mic2:

                recognizer.adjust_for_ambient_noise(mic2, duration=0.2)
                audioo = recognizer.listen(mic2)

                texto = recognizer.recognize_google(audioo)
                texto = texto.lower()

                voz.say(f"He escuchado {texto}")
                voz.runAndWait()
                sys.exit(0)
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            voz.say("no entendi")
            voz.runAndWait()
