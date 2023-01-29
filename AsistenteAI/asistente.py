from neuralintents import GenericAssistant

from Funciones.busqueda import funcionejemplo2, funcionEjemplo


class Asistente(GenericAssistant):

    def __init__(self):
        self.mapa_funciones = {'greeting': funcionEjemplo, 'goodbye': funcionejemplo2}
        GenericAssistant.__init__(self, intents='./IntentsJSON/intents.json', intent_methods=self.mapa_funciones)


