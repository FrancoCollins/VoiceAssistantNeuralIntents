import speech_recognition
from neuralintents import GenericAssistant
import pyttsx3
from pyttsx3 import Engine
import json

from intentsJSON.intent import intent


class Asistente(GenericAssistant):
    username: str
    map_function: dict
    recognizer: speech_recognition.Recognizer
    _voz: Engine
    assistant_name: str
    languages = {"ES": 0, "EN": 1}

    def __init__(self):
        self.username = "user"
        self.functions_map = {'goodbye': self.hibernate}
        GenericAssistant.__init__(self, intents='./intentsJSON/intents_EN.json', intent_methods=self.functions_map)
        self.recognizer = speech_recognition.Recognizer()
        self._voz = pyttsx3.init()
        voice = self._voz.getProperty('voices')
        self._voz.setProperty('voice', voice[self.languages["EN"]].id)
        self._voz.setProperty('rate', 150)
        self.assistant_name = "assistant"

    def say(self, string: str) -> None:
        """Outputs the string simulating the assistant's voice\n
        string :arg -> The message the assistant is will give as audio output"""
        self._voz.say(string)
        self._voz.runAndWait()

    def respond(self, command: str) -> None:
        """ Executes the command given by the user\n
         command :arg -> The command given by the user"""
        answer = self.request(command)
        if answer is not None:
            self.say(answer)

    def greet(self) -> None:
        """The output voice greets the user based on the name
        the assistant previously knows"""
        self.say(f"hello {self.username}")

    def listen(self) -> str:
        """ Starts listening to user input.\n
            Returns the message heard. """
        try:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = self.recognizer.listen(mic)
                mensaje = self.recognizer.recognize_google(audio, language="es-US")
                mensaje = mensaje.lower()

            return mensaje

        except speech_recognition.UnknownValueError:
            return "Error"

    def hibernate(self) -> None:
        """ Enters a hibernation state.\n
            To get out of hibernation, the user should call
            the assistant by name."""
        shouldHibernate = True
        self.say("Hibernating")
        while shouldHibernate:
            if self.listen().find(self.assistant_name) != -1:
                shouldHibernate = False
                self.say(f"Im back! What can I do for you, {self.username}")

    def auto_learn(self, tag: str, pattern: str, response: str) -> None:
        """This method adds tags, patterns and responses given by the user\n
        and the searches result in the Intents JSON file\n
        if the tag already exists it appends the partern and response in the object

        tag :arg -> is the identifier for the intention of the user, is how it is labeled in the JSON file\n
        pattern: arg -> is the pattern the user gave to the assistant, the user expressions
        response :arg -> is the response found by the assistant to the user pattern"""
        intents = []
        file = open('./intentsJSON/intents_EN.json', 'r')
        data = json.load(file)
        exists = False
        for element in data['intents']:
            objectIntent = intent(element['tag'], element['patterns'], element['responses'])
            intents.append(objectIntent)
            if objectIntent.tag == tag:
                exists = True
                if pattern not in objectIntent.patterns:
                    objectIntent.patterns.append(pattern)
                if response not in objectIntent.responses:
                    objectIntent.responses.append(response)
        file.close()

        with open('./intentsJSON/intents_EN.json', 'w') as file:
            if not exists:
                data['intents'].append({
                    'tag': tag,
                    'patterns': [pattern],
                    'responses': [response]})
            json.dump(data, file, indent=3)
            file.close()

        self.train_model()
        self.save_model()
