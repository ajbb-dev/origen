from MVC.Modelo.modelo_pago import ModeloPago

class ControladorPago:

    def __init__(self):
        self.modelo = ModeloPago()

    def obtener_pagos(self):
        return self.modelo.obtener_pagos()

    def obtener_pagos_cliente(self, cliente):
        return self.modelo.obtener_pagos_cliente(cliente)

    def registrar_pago(self, cliente, membresia, monto):
        self.modelo.registrar_pago(cliente, membresia, monto)