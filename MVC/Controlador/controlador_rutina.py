from MVC.Modelo.modelo_rutina import (
    ModeloRutina
)


class ControladorRutina:

    def __init__(self):
        self.modelo = ModeloRutina()

    def obtener_rutinas(self):
        return self.modelo.obtener_rutinas()

    def obtener_rutinas_cliente(
        self,
        cliente
    ):
        return self.modelo.obtener_rutinas_cliente(
            cliente
        )

    def obtener_rutina_hoy(
        self,
        cliente
    ):
        return self.modelo.obtener_rutina_hoy(
            cliente
        )

    def obtener_rutina_reservacion(
        self,
        cliente,
        fecha,
        hora
    ):

        return self.modelo.obtener_rutina_reservacion(
            cliente,
            fecha,
            hora
        )

    def obtener_ejercicios(
        self,
        cancha,
        objetivo
    ):

        return self.modelo.obtener_ejercicios(
            cancha,
            objetivo
        )

    def obtener_objetivos(
        self,
        cancha
    ):

        return self.modelo.obtener_objetivos(
            cancha
        )

    def agregar_rutina(
        self,
        cliente,
        entrenador,
        cancha,
        objetivo,
        ejercicios,
        fecha,
        hora
    ):

        self.modelo.agregar_rutina(
            cliente,
            entrenador,
            cancha,
            objetivo,
            ejercicios,
            fecha,
            hora
        )