from MVC.Modelo.modelo_cancha import ModeloCancha

class ControladorCancha:

    def __init__(self):
        self.modelo = ModeloCancha()

    def obtener_canchas(self):
        return self.modelo.obtener_canchas()

    def cambiar_estado(self, cancha):
        self.modelo.cambiar_estado(cancha)