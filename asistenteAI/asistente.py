import speech_recognition
from neuralintents import GenericAssistant
import pyttsx3
from pyttsx3 import Engine
import wikipedia
import json

import search
from intentsJSON.intent import intent

languages = {"es": 0, "en": 1}


class Asistente(GenericAssistant):
    username: str
    map_function: dict
    recognizer: speech_recognition.Recognizer
    _voz: Engine
    assistant_name: str
    language = "en"

    def __init__(self):
        self.username = "user"
        self.functions_map = {'goodbye': self.hibernate, 'google': self.google_search}
        GenericAssistant.__init__(self, intents=f'./intentsJSON/{self.language}/intents.json', intent_methods=self.functions_map)
        self.recognizer = speech_recognition.Recognizer()
        self._voz = pyttsx3.init()

        # noinspection PyTypeChecker
        voice: list = self._voz.getProperty('voices')

        self._voz.setProperty('voice', voice[languages[self.language]].id)
        self._voz.setProperty('rate', 150)

        wikipedia.set_lang("en")

        self.assistant_name = "assistant"

    def say(self, string: str) -> None:
        """Outputs the string simulating the assistant's voice\n
        :arg string The message the assistant is will give as audio output"""
        self._voz.say(string)
        self._voz.runAndWait()

    def respond(self, command: str) -> None:
        """ Executes the command given by the user.
        :arg command The command given by the user"""
        answer = self.request(command)
        if answer is not None:
            self.say(answer)

    def greet(self) -> None:
        """The output voice greets the user based on the name
        the assistant previously knows"""
        self.say(f"hello {self.username}")

    def listen(self) -> str:
        """ Starts listening to user input.\n
            Returns the message heard."""
        try:
            with speech_recognition.Microphone() as mic:
                self.recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                audio = self.recognizer.listen(mic)
                mensaje = self.recognizer.recognize_google(audio, language="en-US")
                mensaje = mensaje.lower()

            return mensaje

        except speech_recognition.UnknownValueError:
            return "Error"

    def hibernate(self) -> None:
        """ Enters a hibernation state.\n
            To get out of hibernation, the user should call
            the assistant by name."""
        should_hibernate = True
        self.say("Hibernating")
        while should_hibernate:
            if self.listen().find(self.assistant_name) != -1:
                should_hibernate = False
                self.say(f"Im back! What can I do for you, {self.username}")

    def auto_learn(self, tag: str, pattern: str, response: str) -> None:
        """This method adds tags, patterns and responses given by the user\n
        and the searches result in the Intents JSON file\n
        if the tag already exists it appends the partern and response in the object

        tag :arg -> is the identifier for the intention of the user, is how it is labeled in the JSON file\n
        pattern: arg -> is the pattern the user gave to the assistant, the user expressions
        response :arg -> is the response found by the assistant to the user pattern"""
        intents = []
        file = open(f'./intentsJSON/{self.language}/intents_searches.json', 'r')
        data = json.load(file)
        exists = False
        for element in data['intents']:
            object_intent = intent(element['tag'], element['patterns'], element['responses'])
            intents.append(object_intent)
            if object_intent.tag == tag:
                exists = True
                if pattern not in object_intent.patterns:
                    object_intent.patterns.append(pattern)
                if response not in object_intent.responses:
                    object_intent.responses.append(response)
        file.close()

        with open('./intentsJSON/intents.json', 'w') as file:
            if not exists:
                data['intents'].append({
                    'tag': tag,
                    'patterns': [pattern],
                    'responses': [response]})
            json.dump(data, file, indent=3)
            file.close()



        self.train_model()
        self.save_model()

    def google_search(self):

        self.say("I'm listening...")
        query = self.listen()

        while query == "Error":
            self.say("I couldn't hear you. Please say it again.")
            query = self.listen()

        result = search.search(query, language=self.language)

        self.say(result)
