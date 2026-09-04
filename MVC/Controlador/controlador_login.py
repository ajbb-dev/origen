from MVC.Modelo.modelo_login import ModeloLogin

class ControladorLogin:

    def __init__(self):
        self.modelo = ModeloLogin()

    def verificar_login(self, login, password):
        return self.modelo.verificar_usuario(login, password)