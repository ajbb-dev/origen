from MVC.Modelo.modelo_clientes import ModeloClientes


class ControladorClientes:

    def __init__(self):
        self.modelo = ModeloClientes()

    def obtener_clientes(self):
        return self.modelo.obtener_clientes()

    def validar_cliente(self, nombre, cedula, telefono, password):
        return self.modelo.validar_cliente(
            nombre,
            cedula,
            telefono,
            password
        )

    def agregar_cliente(self, cliente, password):
        self.modelo.agregar_cliente(cliente, password)

    def eliminar_cliente(self, cliente):
        self.modelo.eliminar_cliente(cliente)