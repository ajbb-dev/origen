from MVC.Modelo.modelo_entrenador import ModeloEntrenador

class ControladorEntrenador:

    def __init__(self):
        self.modelo = ModeloEntrenador()

    def obtener_entrenadores(self):
        return self.modelo.obtener_entrenadores()
    
    def validar_entrenador(self, cedula, telefono):
        return self.modelo.validar_entrenador(
            cedula,
            telefono
        )

    def agregar_entrenador(self, entrenador, password):
        self.modelo.agregar_entrenador(entrenador, password)

    def eliminar_entrenador(self, entrenador):
        self.modelo.eliminar_entrenador(entrenador)