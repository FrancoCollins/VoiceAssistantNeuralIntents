from asistenteAI.asistente import Asistente

if __name__ == '__main__':

    assistant: Asistente = Asistente()
    assistant.load_model(assistant.model_name)
    assistant.greet()

    while True:
        message = assistant.listen()
        assistant.respond(message)
