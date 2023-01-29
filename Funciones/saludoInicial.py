import speech_recognition

from AsistenteAI.asistente import asistente
from Funciones.busqueda import voz


def start():
    try:
        recognizer = speech_recognition.Recognizer()
        voz.say("hola Franco")
        voz.runAndWait()
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            mensaje = recognizer.recognize_google(audio)
            mensaje = mensaje.lower()

        asistente.request(mensaje)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
