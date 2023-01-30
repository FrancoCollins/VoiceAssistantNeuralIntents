from asistenteAI.asistente import Asistente

if __name__ == '__main__':

    asistent: Asistente = Asistente()
    asistent.load_model(asistent.model_name)
    asistent.greet()

    while True:
        message = asistent.listen()
        asistent.respond(message)

