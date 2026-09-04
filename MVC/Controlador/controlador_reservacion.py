from MVC.Modelo.modelo_reservacion import ModeloReservacion

class ControladorReservacion:

    def __init__(self):
        self.modelo = ModeloReservacion()

    def obtener_reservaciones(self):
        return self.modelo.obtener_reservaciones()

    def obtener_reservaciones_cliente(self, cliente):
        return self.modelo.obtener_reservaciones_cliente(cliente)

    def agregar_reservacion(self, reservacion):
        self.modelo.agregar_reservacion(reservacion)

    def cancelar_reservacion(self, reservacion):
        self.modelo.cancelar_reservacion(reservacion)

    def verificar_disponibilidad(self, cancha, fecha, hora):
        return self.modelo.verificar_disponibilidad(cancha, fecha, hora)