from tkinter import *
from tkinter import messagebox
from MVC.Controlador.controlador_login import ControladorLogin
from MVC.Vista.vista_administrador import abrir_ventana_administrador
from MVC.Vista.vista_entrenador import abrir_ventana_entrenador
from MVC.Vista.vista_usuario import abrir_ventana_usuario
from MVC.Vista.estilos import *

controlador = ControladorLogin()

def iniciar_login():
    ventana = Tk()
    ventana.title("Plataforma deportiva")
    ventana.geometry("900x600")
    ventana.config(bg=COLOR_FONDO)
    ventana.resizable(False, False)

    def cerrar_ventana(ventana_rol):
        ventana_rol.destroy()
        ventana.deiconify()

    def validar_login(nuevo_valor):
        if nuevo_valor == "": return True
        if not nuevo_valor.isdigit(): return False
        if len(nuevo_valor) > 10: return False
        return True

    def validar_password(nuevo_valor):
        if nuevo_valor == "": return True
        if nuevo_valor.startswith(" "): return False
        if len(nuevo_valor) > 30: return False
        return True

    validacion_login = ventana.register(validar_login)
    validacion_password = ventana.register(validar_password)

    def verificar_login():
        login = entrada_login.get().strip()
        password = entrada_password.get()

        if not login or not password.strip():
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        if len(login) < 6:
            messagebox.showwarning("Error", "La cédula debe tener mínimo 6 dígitos")
            return
        if len(password.strip()) < 6:
            messagebox.showwarning("Error", "La contraseña debe tener mínimo 6 caracteres")
            return

        resultado, datos = controlador.verificar_login(login, password.strip())

        if resultado == "administrador":
            ventana.withdraw()
            abrir_ventana_administrador(cerrar_ventana)
        elif resultado == "entrenador":
            ventana.withdraw()
            abrir_ventana_entrenador(cerrar_ventana, datos)
        elif resultado == "usuario":
            ventana.withdraw()
            abrir_ventana_usuario(cerrar_ventana, datos)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # CONTENEDOR PRINCIPAL
    contenedor = Frame(ventana, bg=COLOR_FONDO)
    contenedor.pack(expand=True)

    # PANEL LOGIN
    panel = Frame(contenedor, bg=COLOR_PANEL, padx=50, pady=40)
    panel.pack()

    # TITULOS
    Label(panel, text="⚽ CENTRO DEPORTIVO", font=FUENTE_TITULO, fg=COLOR_TEXTO, bg=COLOR_PANEL).pack(pady=(0, 10))
    Label(panel, text="Iniciar sesión", font=FUENTE_SUBTITULO, fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(pady=(0, 30))

    # LOGIN
    Label(panel, text="Cédula", font=FUENTE_LABEL, fg=COLOR_TEXTO, bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_login = Entry(panel, font=FUENTE_INPUT, width=ANCHO_INPUT, bd=0, relief="flat", validate="key", validatecommand=(validacion_login, "%P"))
    entrada_login.pack(ipady=8, pady=(5, 20))

    # PASSWORD
    Label(panel, text="Contraseña", font=FUENTE_LABEL, fg=COLOR_TEXTO, bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_password = Entry(panel, show="*", font=FUENTE_INPUT, width=ANCHO_INPUT, bd=0, relief="flat", validate="key", validatecommand=(validacion_password, "%P"))
    entrada_password.pack(ipady=8, pady=(5, 30))

    # BOTON LOGIN
    Button(panel, text="INGRESAR", command=verificar_login, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", activebackground=COLOR_BOTON_HOVER, activeforeground="white", relief="flat", cursor="hand2", padx=30, pady=10).pack(fill="x")

    ventana.mainloop()