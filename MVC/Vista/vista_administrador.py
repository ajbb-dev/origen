from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
import re
from MVC.Vista.estilos import *

from MVC.Controlador.controlador_clientes import ControladorClientes
from MVC.Controlador.controlador_cancha import ControladorCancha
from MVC.Controlador.controlador_entrenador import ControladorEntrenador
from MVC.Controlador.controlador_reservacion import ControladorReservacion  
from MVC.Controlador.controlador_pago import ControladorPago
from MVC.Controlador.controlador_rutina import ControladorRutina

def abrir_ventana_administrador(cerrar_ventana):
    controlador_clientes = ControladorClientes()
    controlador_cancha = ControladorCancha()
    controlador_entrenador = ControladorEntrenador()
    controlador_reservacion = ControladorReservacion()
    controlador_pago = ControladorPago()

    ventana_administrador = Toplevel()
    ventana_administrador.title("Administración Deportiva")
    ventana_administrador.geometry("1200x700")
    ventana_administrador.config(bg=COLOR_FONDO)
    ventana_administrador.resizable(False, False)
    ventana_administrador.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(ventana_administrador))

    # ==================================
    # CONTENEDOR PRINCIPAL Y LAYOUT
    # ==================================
    contenedor = Frame(ventana_administrador, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True)

    navegacion = Frame(contenedor, bg=COLOR_PANEL, width=250)
    navegacion.pack(side="left", fill="y")
    navegacion.pack_propagate(False)

    informacion = Frame(contenedor, bg=COLOR_FONDO)
    informacion.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # ==================================
    # ENCABEZADO PANEL LATERAL
    # ==================================
    Label(navegacion,text="⚽ ADMINISTRACIÓN",font=("Arial", 17, "bold"),fg=COLOR_TEXTO,bg=COLOR_PANEL).pack(pady=(30, 10))
    Label(navegacion, text="Centro Deportivo", font=FUENTE_SUBTITULO, fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(pady=(0, 30))

    # ==================================
    # BOTONES MENÚ LATERAL
    # ==================================
    Button(navegacion, text="👥 Clientes", command=lambda: cargar_clientes(informacion, controlador_clientes), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x", padx=20, pady=6)
    Button(navegacion, text="🏟 Canchas", command=lambda: cargar_canchas(informacion, controlador_cancha), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x", padx=20, pady=6)
    Button(navegacion, text="💳 Pagos", command=lambda: cargar_pagos(informacion, controlador_pago, controlador_clientes), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x", padx=20, pady=6)
    Button(navegacion, text="📅 Reservaciones", command=lambda: cargar_reservaciones(informacion, controlador_reservacion, controlador_clientes), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x", padx=20, pady=6)
    Button(navegacion, text="🏋 Base de integrantes", command=lambda: cargar_base_integrantes(informacion, controlador_entrenador), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x", padx=20, pady=6)

    # ==================================
    # VISTA DE BIENVENIDA INICIAL
    # ==================================
    Label(informacion, text="Bienvenido al panel de administración", font=("Arial", 22, "bold"), fg="white", bg=COLOR_FONDO).pack(pady=(120, 10))
    Label(informacion, text="Selecciona una opción del menú lateral", font=("Arial", 14), fg=COLOR_SUBTITULO, bg=COLOR_FONDO).pack()

def limpiar(informacion):
    for widget in informacion.winfo_children():
        widget.destroy()

def cargar_clientes(informacion, controlador):
    limpiar(informacion)
    Label(informacion, text="Clientes").grid(row=0, column=0)
    Button(informacion, text="Agregar Cliente", command=lambda: agregar_cliente(informacion, controlador)).grid(row=1, column=0)

    clientes = controlador.obtener_clientes()
    if not clientes:
        Label(informacion, text="No hay clientes registrados").grid(row=2, column=0)
        return

    # Encabezados
    Label(informacion, text="Nombre").grid(row=2, column=0)
    Label(informacion, text="Cédula").grid(row=2, column=1)
    Label(informacion, text="Teléfono").grid(row=2, column=2)

    for i, cliente in enumerate(clientes):
        Label(informacion, text=cliente["nombre"]).grid(row=i + 3, column=0)
        Label(informacion, text=cliente["cedula"]).grid(row=i + 3, column=1)
        Label(informacion, text=cliente["telefono"]).grid(row=i + 3, column=2)
        Button(informacion, text="Eliminar", command=lambda c=cliente: eliminar_cliente(c, informacion, controlador)).grid(row=i + 3, column=3)

def cargar_clientes(informacion, controlador):
    limpiar(informacion)

    # ==================================
    # TITULO Y BOTÓN AGREGAR
    # ==================================
    Label(informacion, text="👥 Gestión de Clientes", font=("Arial", 20, "bold"), fg="white", bg=COLOR_FONDO).pack(anchor="w", pady=(10, 20))
    Button(informacion, text="+ Agregar Cliente", command=lambda: agregar_cliente(informacion, controlador), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", padx=20, pady=8).pack(anchor="w", pady=(0, 20))

    clientes = controlador.obtener_clientes()

    if not clientes:
        Label(informacion, text="No hay clientes registrados", font=("Arial", 13), fg=COLOR_SUBTITULO, bg=COLOR_FONDO).pack(pady=20)
        return

    # ==================================
    # CONTENEDOR TABLA Y ENCABEZADOS
    # ==================================
    tabla = Frame(informacion, bg=COLOR_PANEL, padx=15, pady=15)
    tabla.pack(fill="x")

    encabezados = ["Nombre", "Cédula", "Teléfono", "Acción"]
    for col, texto in enumerate(encabezados):
        Label(tabla, text=texto, font=("Arial", 11, "bold"), fg="white", bg=COLOR_PANEL, padx=15, pady=10).grid(row=0, column=col, sticky="w")

    # ==================================
    # DATOS CLIENTES
    # ==================================
    for i, cliente in enumerate(clientes):
        fila = i + 1
        Label(tabla, text=cliente["nombre"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=0, padx=15, pady=8, sticky="w")
        Label(tabla, text=cliente["cedula"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=1, padx=15, pady=8, sticky="w")
        Label(tabla, text=cliente["telefono"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=2, padx=15, pady=8, sticky="w")
        
        Button(tabla, text="Eliminar", command=lambda c=cliente: eliminar_cliente(c, informacion, controlador), font=("Arial", 10, "bold"), bg="#dc2626", fg="white", relief="flat", cursor="hand2", padx=10).grid(row=fila, column=3, padx=10, pady=5)


def agregar_cliente(informacion, controlador):
    ventana_cliente = Toplevel()
    ventana_cliente.title("Agregar Cliente")
    ventana_cliente.geometry("500x500")
    ventana_cliente.config(bg=COLOR_FONDO)
    ventana_cliente.resizable(False, False)

    # ==================================
    # VALIDACIONES EN LÍNEA
    # ==================================
    def validar_nombre(nuevo_valor):
        if nuevo_valor == "": return True
        if nuevo_valor.startswith(" ") or "  " in nuevo_valor or len(nuevo_valor) > 50: return False
        return bool(re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", nuevo_valor))

    def validar_cedula(nuevo_valor):
        return True if nuevo_valor == "" else (nuevo_valor.isdigit() and len(nuevo_valor) <= 10)

    def validar_telefono(nuevo_valor):
        return True if nuevo_valor == "" else (nuevo_valor.isdigit() and len(nuevo_valor) <= 10)

    def validar_password(nuevo_valor):
        return True if nuevo_valor == "" else (not nuevo_valor.startswith(" ") and len(nuevo_valor) <= 30)

    validacion_nombre = ventana_cliente.register(validar_nombre)
    validacion_cedula = ventana_cliente.register(validar_cedula)
    validacion_telefono = ventana_cliente.register(validar_telefono)
    validacion_password = ventana_cliente.register(validar_password)

    # ==================================
    # CONTENEDOR CENTRAL Y PANEL FORMULARIO
    # ==================================
    contenedor = Frame(ventana_cliente, bg=COLOR_FONDO)
    contenedor.pack(expand=True)

    panel = Frame(contenedor, bg=COLOR_PANEL, padx=40, pady=35)
    panel.pack()

    Label(panel, text="👤 Nuevo Cliente", font=("Arial", 18, "bold"), fg="white", bg=COLOR_PANEL).pack(pady=(0, 25))

    # Campos del Formulario (Label + Entry)
    Label(panel, text="Nombre", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_nombre = Entry(panel, font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_nombre, "%P"))
    entrada_nombre.pack(ipady=7, pady=(5, 15))

    Label(panel, text="Cédula", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_cedula = Entry(panel, font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_cedula, "%P"))
    entrada_cedula.pack(ipady=7, pady=(5, 15))

    Label(panel, text="Teléfono", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_telefono = Entry(panel, font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_telefono, "%P"))
    entrada_telefono.pack(ipady=7, pady=(5, 15))

    Label(panel, text="Contraseña", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_password = Entry(panel, show="*", font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_password, "%P"))
    entrada_password.pack(ipady=7, pady=(5, 25))

    # ==================================
    # ACCIÓN GUARDAR
    # ==================================
    def guardar_cliente():
        nombre = entrada_nombre.get().strip()
        cedula = entrada_cedula.get().strip()
        telefono = entrada_telefono.get().strip()
        password = entrada_password.get()

        if not nombre or not cedula or not telefono or not password.strip():
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        if len(nombre) < 3:
            messagebox.showwarning("Error", "El nombre debe tener mínimo 3 caracteres")
            return
        if len(cedula) < 6:
            messagebox.showwarning("Error", "La cédula debe tener mínimo 6 dígitos")
            return
        if len(telefono) != 10:
            messagebox.showwarning("Error", "El teléfono debe tener exactamente 10 dígitos")
            return
        if len(password.strip()) < 6:
            messagebox.showwarning("Error", "La contraseña debe tener mínimo 6 caracteres")
            return

        clientes = controlador.obtener_clientes()
        controlador_entrenador = ControladorEntrenador()
        entrenadores = controlador_entrenador.obtener_entrenadores()

        if any(c["cedula"] == cedula for c in clientes) or any(e["cedula"] == cedula for e in entrenadores):
            messagebox.showwarning("Error", "Esta cédula ya existe")
            return
        if any(c["telefono"] == telefono for c in clientes) or any(e["telefono"] == telefono for e in entrenadores):
            messagebox.showwarning("Error", "Este teléfono ya existe")
            return

        nuevo_cliente = {
            "nombre": nombre,
            "cedula": cedula,
            "telefono": telefono,
            "password": password.strip()
        }

        controlador.agregar_cliente(nuevo_cliente, password.strip())
        messagebox.showinfo("Éxito", "Cliente agregado correctamente")
        ventana_cliente.destroy()
        cargar_clientes(informacion, controlador)

    Button(panel, text="GUARDAR CLIENTE", command=guardar_cliente, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x")

def eliminar_cliente(cliente, informacion, controlador):
    controlador_reservacion = ControladorReservacion()
    reservaciones = controlador_reservacion.obtener_reservaciones()

    tiene_reservas = any(r["cliente"]["cedula"] == cliente["cedula"] and r["estado"] == "activa" for r in reservaciones)
    if tiene_reservas:
        messagebox.showwarning("Error", "No puedes eliminar este cliente porque tiene reservaciones activas")
        return

    if messagebox.askyesno("Confirmar eliminación", "¿Seguro que deseas eliminar este cliente?"):
        controlador.eliminar_cliente(cliente)
        cargar_clientes(informacion, controlador)      

def cargar_canchas(informacion, controlador):
    limpiar(informacion)

    # ==================================
    # TITULO
    # ==================================
    Label(informacion, text="🏟 Gestión de Canchas", font=("Arial", 20, "bold"), fg="white", bg=COLOR_FONDO).pack(anchor="w", pady=(10, 20))

    canchas = controlador.obtener_canchas()

    if not canchas:
        Label(informacion, text="No hay canchas registradas", font=("Arial", 13), fg=COLOR_SUBTITULO, bg=COLOR_FONDO).pack(pady=20)
        return

    # ==================================
    # CONTENEDOR TABLA Y ENCABEZADOS
    # ==================================
    tabla = Frame(informacion, bg=COLOR_PANEL, padx=15, pady=15)
    tabla.pack(fill="x")

    encabezados = ["Sector", "Ocupación", "Disponibilidad", "Estado", "Acción"]
    for col, texto in enumerate(encabezados):
        Label(tabla, text=texto, font=("Arial", 11, "bold"), fg="white", bg=COLOR_PANEL, padx=15, pady=10).grid(row=0, column=col, sticky="w")

    # ==================================
    # DATOS CANCHAS
    # ==================================
    for i, cancha in enumerate(canchas):
        fila = i + 1

        disponible = "Disponible" if cancha["ocupacion_actual"] < cancha["capacidad"] and cancha["activo"] else "No disponible"
        estado = "Activa" if cancha["activo"] else "Inactiva"

        # Celdas de datos con Grid unificado
        Label(tabla, text=cancha["sector"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=0, padx=15, pady=8, sticky="w")
        Label(tabla, text=f"{cancha['ocupacion_actual']}/{cancha['capacidad']}", font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=1, padx=15, pady=8, sticky="w")
        Label(tabla, text=disponible, font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=2, padx=15, pady=8, sticky="w")
        Label(tabla, text=estado, font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=3, padx=15, pady=8, sticky="w")
        
        # Botón dinámico activar/desactivar
        Button(tabla, text="Desactivar" if cancha["activo"] else "Activar", command=lambda c=cancha: cambiar_estado_cancha(c, informacion, controlador), font=("Arial", 10, "bold"), bg="#dc2626" if cancha["activo"] else COLOR_BOTON, fg="white", relief="flat", cursor="hand2", padx=10).grid(row=fila, column=4, padx=10, pady=5)

def cambiar_estado_cancha(cancha, informacion, controlador):
    if cancha["activo"]:
        controlador_reservacion = ControladorReservacion()
        reservaciones = controlador_reservacion.obtener_reservaciones()

        if any(r["cancha"] == cancha["sector"] and r["estado"] == "activa" for r in reservaciones):
            messagebox.showwarning("Error", "No puedes desactivar esta cancha porque tiene reservaciones activas")
            return

    controlador.cambiar_estado(cancha)
    cargar_canchas(informacion, controlador)

def cargar_base_integrantes(informacion, controlador):
    limpiar(informacion)

    # ==================================
    # TITULO Y BOTÓN AGREGAR
    # ==================================
    Label(informacion, text="🏋 Gestión de Entrenadores", font=("Arial", 20, "bold"), fg="white", bg=COLOR_FONDO).pack(anchor="w", pady=(10, 20))
    Button(informacion, text="+ Agregar Entrenador", command=lambda: agregar_entrenador(informacion, controlador), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", padx=20, pady=8).pack(anchor="w", pady=(0, 20))

    entrenadores = controlador.obtener_entrenadores()

    if not entrenadores:
        Label(informacion, text="No hay entrenadores registrados", font=("Arial", 13), fg=COLOR_SUBTITULO, bg=COLOR_FONDO).pack(pady=20)
        return

    # ==================================
    # TABLA Y ENCABEZADOS
    # ==================================
    tabla = Frame(informacion, bg=COLOR_PANEL, padx=15, pady=15)
    tabla.pack(fill="x")

    encabezados = ["Nombre", "Cédula", "Teléfono", "Especialidad", "Acción"]
    for col, texto in enumerate(encabezados):
        Label(tabla, text=texto, font=("Arial", 11, "bold"), fg="white", bg=COLOR_PANEL, padx=15, pady=10).grid(row=0, column=col, sticky="w")

    # ==================================
    # DATOS ENTRENADORES
    # ==================================
    for i, entrenador in enumerate(entrenadores):
        fila = i + 1
        Label(tabla, text=entrenador["nombre"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=0, padx=15, pady=8, sticky="w")
        Label(tabla, text=entrenador["cedula"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=1, padx=15, pady=8, sticky="w")
        Label(tabla, text=entrenador["telefono"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=2, padx=15, pady=8, sticky="w")
        Label(tabla, text=entrenador["especialidad"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=3, padx=15, pady=8, sticky="w")
        
        Button(tabla, text="Eliminar", command=lambda e=entrenador: eliminar_entrenador(e, informacion, controlador), font=("Arial", 10, "bold"), bg="#dc2626", fg="white", relief="flat", cursor="hand2", padx=10).grid(row=fila, column=4, padx=10, pady=5)


def agregar_entrenador(informacion, controlador):
    ventana_entrenador = Toplevel()
    ventana_entrenador.title("Agregar Entrenador")
    ventana_entrenador.geometry("520x580")
    ventana_entrenador.config(bg=COLOR_FONDO)
    ventana_entrenador.resizable(False, False)

    # ==================================
    # VALIDACIONES EN LÍNEA
    # ==================================
    def validar_nombre(nuevo_valor):
        if nuevo_valor == "": return True
        if nuevo_valor.startswith(" ") or "  " in nuevo_valor or len(nuevo_valor) > 50: return False
        return bool(re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ ]+$", nuevo_valor))

    def validar_cedula(nuevo_valor):
        return True if nuevo_valor == "" else (nuevo_valor.isdigit() and len(nuevo_valor) <= 10)

    def validar_telefono(nuevo_valor):
        return True if nuevo_valor == "" else (nuevo_valor.isdigit() and len(nuevo_valor) <= 10)

    def validar_password(nuevo_valor):
        return True if nuevo_valor == "" else (not nuevo_valor.startswith(" ") and len(nuevo_valor) <= 30)

    validacion_nombre = ventana_entrenador.register(validar_nombre)
    validacion_cedula = ventana_entrenador.register(validar_cedula)
    validacion_telefono = ventana_entrenador.register(validar_telefono)
    validacion_password = ventana_entrenador.register(validar_password)

    # ==================================
    # CONTENEDOR Y FORMULARIO
    # ==================================
    contenedor = Frame(ventana_entrenador, bg=COLOR_FONDO)
    contenedor.pack(expand=True)

    panel = Frame(contenedor, bg=COLOR_PANEL, padx=40, pady=35)
    panel.pack()

    Label(panel, text="🏋 Nuevo Entrenador", font=("Arial", 18, "bold"), fg="white", bg=COLOR_PANEL).pack(pady=(0, 25))

    # Campos del Formulario
    Label(panel, text="Nombre", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_nombre = Entry(panel, font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_nombre, "%P"))
    entrada_nombre.pack(ipady=7, pady=(5, 15))

    Label(panel, text="Cédula", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_cedula = Entry(panel, font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_cedula, "%P"))
    entrada_cedula.pack(ipady=7, pady=(5, 15))

    Label(panel, text="Teléfono", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_telefono = Entry(panel, font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_telefono, "%P"))
    entrada_telefono.pack(ipady=7, pady=(5, 15))

    Label(panel, text="Especialidad", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    especialidad_var = StringVar(ventana_entrenador, value="Futbol")
    opciones = ["Futbol", "Voleibol", "Baloncesto", "Gimnasio", "Piscina"]
    menu = OptionMenu(panel, especialidad_var, *opciones)
    menu.config(font=("Arial", 11), width=28)
    menu.pack(pady=(5, 15))

    Label(panel, text="Contraseña", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_password = Entry(panel, show="*", font=FUENTE_INPUT, width=30, validate="key", validatecommand=(validacion_password, "%P"))
    entrada_password.pack(ipady=7, pady=(5, 25))

    # ==================================
    # ACCIÓN GUARDAR
    # ==================================
    def guardar_entrenador():
        nombre = entrada_nombre.get().strip()
        cedula = entrada_cedula.get().strip()
        telefono = entrada_telefono.get().strip()
        especialidad = especialidad_var.get()
        password = entrada_password.get()

        if not nombre or not cedula or not telefono or not password.strip():
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        if len(nombre) < 3:
            messagebox.showwarning("Error", "El nombre debe tener mínimo 3 caracteres")
            return
        if len(cedula) < 6:
            messagebox.showwarning("Error", "La cédula debe tener mínimo 6 dígitos")
            return
        if len(telefono) != 10:
            messagebox.showwarning("Error", "El teléfono debe tener exactamente 10 dígitos")
            return
        if len(password.strip()) < 6:
            messagebox.showwarning("Error", "La contraseña debe tener mínimo 6 caracteres")
            return

        entrenadores = controlador.obtener_entrenadores()
        controlador_clientes = ControladorClientes()
        clientes = controlador_clientes.obtener_clientes()

        if any(e["cedula"] == cedula for e in entrenadores) or any(c["cedula"] == cedula for c in clientes):
            messagebox.showwarning("Error", "Esta cédula ya existe")
            return
        if any(e["telefono"] == telefono for e in entrenadores) or any(c["telefono"] == telefono for c in clientes):
            messagebox.showwarning("Error", "Este teléfono ya existe")
            return

        nuevo_entrenador = {
            "nombre": nombre,
            "cedula": cedula,
            "telefono": telefono,
            "especialidad": especialidad
        }

        controlador.agregar_entrenador(nuevo_entrenador, password.strip())
        messagebox.showinfo("Éxito", "Entrenador agregado correctamente")
        ventana_entrenador.destroy()
        cargar_base_integrantes(informacion, controlador)

    Button(panel, text="GUARDAR ENTRENADOR", command=guardar_entrenador, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x")

    def guardar_entrenador():
        nombre = entrada_nombre.get().strip()
        cedula = entrada_cedula.get().strip()
        telefono = entrada_telefono.get().strip()
        especialidad = especialidad_var.get()
        password = entrada_password.get()

        if not nombre or not cedula or not telefono or not password.strip():
            messagebox.showwarning("Error", "Todos los campos son obligatorios")
            return
        if len(nombre) < 3:
            messagebox.showwarning("Error", "El nombre debe tener mínimo 3 caracteres")
            return
        if len(cedula) < 6:
            messagebox.showwarning("Error", "La cédula debe tener mínimo 6 dígitos")
            return
        if len(telefono) != 10:
            messagebox.showwarning("Error", "El teléfono debe tener exactamente 10 dígitos")
            return
        if len(password.strip()) < 6:
            messagebox.showwarning("Error", "La contraseña debe tener mínimo 6 caracteres")
            return

        entrenadores = controlador.obtener_entrenadores()
        controlador_clientes = ControladorClientes()
        clientes = controlador_clientes.obtener_clientes()

        if any(e["cedula"] == cedula for e in entrenadores) or any(c["cedula"] == cedula for c in clientes):
            messagebox.showwarning("Error", "Esta cédula ya existe")
            return
        if any(e["telefono"] == telefono for e in entrenadores) or any(c["telefono"] == telefono for c in clientes):
            messagebox.showwarning("Error", "Este teléfono ya existe")
            return

        nuevo_entrenador = {"nombre": nombre, "cedula": cedula, "telefono": telefono, "especialidad": especialidad}
        controlador.agregar_entrenador(nuevo_entrenador, password.strip())

        messagebox.showinfo("Éxito", "Entrenador agregado correctamente")
        ventana_entrenador.destroy()
        cargar_base_integrantes(informacion, controlador)

    Button(ventana_entrenador, text="Guardar", command=guardar_entrenador).grid(row=5, column=0, columnspan=2)

def eliminar_entrenador(entrenador, informacion, controlador):
    from MVC.Controlador.controlador_rutina import ControladorRutina
    controlador_rutina = ControladorRutina()
    
    if any(r["entrenador"]["cedula"] == entrenador["cedula"] for r in controlador_rutina.obtener_rutinas()):
        messagebox.showwarning("Error", "No se puede eliminar el entrenador porque tiene rutinas asignadas")
        return

    if messagebox.askyesno("Confirmar eliminación", "¿Seguro que deseas eliminar este entrenador?"):
        controlador.eliminar_entrenador(entrenador)
        messagebox.showinfo("Éxito", "Entrenador eliminado correctamente")
        cargar_base_integrantes(informacion, controlador)

def cargar_reservaciones(informacion, controlador, controlador_clientes):
    limpiar(informacion)

    # ==================================
    # TITULO Y BOTÓN AGREGAR
    # ==================================
    Label(informacion, text="📅 Gestión de Reservaciones", font=("Arial", 18, "bold"), fg="white", bg=COLOR_FONDO).pack(anchor="w", pady=(10, 20))
    Button(informacion, text="+ Nueva Reservación", command=lambda: agregar_reservacion(informacion, controlador, controlador_clientes), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", padx=20, pady=8).pack(anchor="w", pady=(0, 20))

    reservaciones = controlador.obtener_reservaciones()

    if not reservaciones:
        Label(informacion, text="No hay reservaciones registradas", font=("Arial", 13), fg=COLOR_SUBTITULO, bg=COLOR_FONDO).pack(pady=20)
        return

    # ==================================
    # TABLA Y ENCABEZADOS
    # ==================================
    tabla = Frame(informacion, bg=COLOR_PANEL, padx=15, pady=15)
    tabla.pack(fill="both", expand=True)

    encabezados = ["Cliente", "Cancha", "Objetivo", "Fecha", "Hora", "Estado", "Acción"]
    for col, texto in enumerate(encabezados):
        Label(tabla, text=texto, font=("Arial", 11, "bold"), fg="white", bg=COLOR_PANEL, padx=15, pady=10).grid(row=0, column=col, sticky="w")

    # ==================================
    # DATOS RESERVACIONES
    # ==================================
    for i, reservacion in enumerate(reservaciones):
        fila = i + 1
        
        datos = [
            reservacion["cliente"]["nombre"],
            reservacion["cancha"],
            reservacion["objetivo"],
            reservacion["fecha"],
            reservacion["hora"],
            reservacion["estado"]
        ]

        for col, dato in enumerate(datos):
            Label(tabla, text=dato, font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=col, padx=15, pady=8, sticky="w")

        # Botón condicional para cancelar reservación activa
        if reservacion["estado"] == "activa":
            Button(tabla, text="Cancelar", command=lambda r=reservacion: cancelar_reservacion(r, informacion, controlador, controlador_clientes), font=("Arial", 10, "bold"), bg="#dc2626", fg="white", relief="flat", cursor="hand2", padx=10).grid(row=fila, column=6, padx=10, pady=5)

def agregar_reservacion(informacion, controlador, controlador_clientes):
    ventana_reservacion = Toplevel()
    ventana_reservacion.title("Nueva Reservación")
    ventana_reservacion.geometry("760x680")
    ventana_reservacion.config(bg=COLOR_FONDO)
    ventana_reservacion.resizable(False, False)

    hoy = datetime.now()
    max_fecha = hoy + __import__("datetime").timedelta(days=30)
    clientes = controlador_clientes.obtener_clientes()
    controlador_rutina = ControladorRutina()

    # ==================================
    # CONTENEDOR PRINCIPAL Y PANELES
    # ==================================
    principal = Frame(ventana_reservacion, bg=COLOR_FONDO, padx=20, pady=20)
    principal.pack(fill="both", expand=True)

    panel = Frame(principal, bg=COLOR_PANEL, padx=25, pady=25)
    panel.pack(fill="both", expand=True)

    Label(panel, text="📅 Nueva Reservación", font=("Arial", 17, "bold"), fg="white", bg=COLOR_PANEL).pack(pady=(0, 20))

    # Columnas: Contenido Superior (Izquierda / Derecha)
    contenido = Frame(panel, bg=COLOR_PANEL)
    contenido.pack(fill="x")

    izquierda = Frame(contenido, bg=COLOR_PANEL)
    izquierda.pack(side="left", fill="both", expand=True, padx=(0, 15))

    derecha = Frame(contenido, bg=COLOR_PANEL)
    derecha.pack(side="right", fill="both", expand=True)

    # ==================================
    # COLUMNA IZQUIERDA: CLIENTE
    # ==================================
    Label(izquierda, text="Buscar Cliente", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_busqueda = Entry(izquierda, font=FUENTE_INPUT)
    entrada_busqueda.pack(fill="x", ipady=7, pady=(5, 10))

    lista_clientes = Listbox(izquierda, height=10, font=("Arial", 11))
    lista_clientes.pack(fill="both", expand=True)

    def actualizar_lista(*args):
        busqueda = entrada_busqueda.get().lower()
        lista_clientes.delete(0, END)
        for c in clientes:
            if busqueda in c["nombre"].lower() or busqueda in c["cedula"]:
                lista_clientes.insert(END, f"{c['nombre']} | {c['cedula']}")

    actualizar_lista()
    entrada_busqueda.bind("<KeyRelease>", actualizar_lista)

    # ==================================
    # COLUMNA DERECHA: CONFIGURACIÓN
    # ==================================
    # Cancha
    Label(derecha, text="Cancha", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    cancha_var = StringVar(ventana_reservacion, value="Futbol")
    menu_cancha = OptionMenu(derecha, cancha_var, "Futbol", "Voleibol", "Baloncesto", "Gimnasio", "Piscina")
    menu_cancha.config(font=("Arial", 11), width=24)
    menu_cancha.pack(pady=(5, 15))

    # Objetivo
    Label(derecha, text="Objetivo", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    objetivo_var = StringVar(ventana_reservacion, value="Resistencia")
    menu_objetivo = OptionMenu(derecha, objetivo_var, "Resistencia")
    menu_objetivo.config(font=("Arial", 11), width=24)
    menu_objetivo.pack(pady=(5, 15))

    def actualizar_objetivos(*args):
        objetivos = controlador_rutina.obtener_objetivos(cancha_var.get()) + ["El entrenador decide"]
        menu_objetivo["menu"].delete(0, "end")
        for obj in objetivos:
            menu_objetivo["menu"].add_command(label=obj, command=lambda o=obj: objetivo_var.set(o))
        objetivo_var.set(objetivos[0])

    cancha_var.trace("w", actualizar_objetivos)
    actualizar_objetivos()

    # Hora
    Label(derecha, text="Hora", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL).pack(fill="x")
    hora_var = StringVar(ventana_reservacion, value="06:00")
    menu_hora = OptionMenu(derecha, hora_var, "06:00")
    menu_hora.config(font=("Arial", 11), width=24)
    menu_hora.pack(pady=(5, 20))

    # ==================================
    # SECCIÓN INFERIOR: CALENDARIO Y GUARDADO
    # ==================================
    Label(panel, text="Selecciona Fecha", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL).pack(pady=(20, 5))
    calendario = Calendar(panel, selectmode="day", year=hoy.year, month=hoy.month, day=hoy.day, mindate=hoy.date(), maxdate=max_fecha.date())
    calendario.pack()

    def actualizar_horas(*args):
        fecha = datetime.strptime(calendario.get_date(), "%m/%d/%y").date()
        ahora = datetime.now()
        horas_disponibles = [f"{h:02d}:00" for h in range(6, 23) if fecha != ahora.date() or h > ahora.hour]

        menu_hora["menu"].delete(0, "end")
        for hora in horas_disponibles:
            menu_hora["menu"].add_command(label=hora, command=lambda h=hora: hora_var.set(h))
        hora_var.set(horas_disponibles[0] if horas_disponibles else "No hay horas disponibles")

    calendario.bind("<<CalendarSelected>>", actualizar_horas)
    actualizar_horas()

    # ==================================
    # ACCIÓN GUARDAR
    # ==================================
    def guardar_reservacion():
        if not lista_clientes.curselection():
            messagebox.showwarning("Error", "Selecciona un cliente")
            return

        seleccion = lista_clientes.get(lista_clientes.curselection())
        cedula = seleccion.split(" | ")[1]
        cliente = next((c for c in clientes if c["cedula"] == cedula), None)

        if not cliente.get("membresia"):
            messagebox.showwarning("Error", "El cliente no tiene una membresía activa")
            return

        hora = hora_var.get()
        if hora == "No hay horas disponibles":
            messagebox.showwarning("Error", "No hay horas disponibles para hoy")
            return

        cancha = cancha_var.get()
        fecha = datetime.strptime(calendario.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")

        if any(r["cliente"]["cedula"] == cliente["cedula"] and r["fecha"] == fecha and r["hora"] == hora and r["estado"] == "activa" for r in controlador.obtener_reservaciones()):
            messagebox.showwarning("Error", "El cliente ya tiene una reservación en esa fecha y hora")
            return

        if not controlador.verificar_disponibilidad(cancha, fecha, hora):
            messagebox.showerror("Error", "La cancha no está disponible en ese horario")
            return

        controlador.agregar_reservacion({
            "cliente": cliente,
            "cancha": cancha,
            "objetivo": objetivo_var.get(),
            "fecha": fecha,
            "hora": hora,
            "estado": "activa"
        })

        ventana_reservacion.destroy()
        cargar_reservaciones(informacion, controlador, controlador_clientes)

    Button(panel, text="GUARDAR RESERVACIÓN", command=guardar_reservacion, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x", pady=(20, 0))

def cancelar_reservacion(reservacion, informacion, controlador, controlador_clientes):
    if messagebox.askyesno("Confirmar cancelación", "¿Seguro que deseas cancelar esta reservación?"):
        controlador.cancelar_reservacion(reservacion)
        cargar_reservaciones(informacion, controlador, controlador_clientes)

def cargar_pagos(informacion, controlador, controlador_clientes):
    limpiar(informacion)

    # ==================================
    # TITULO Y BOTÓN REGISTRAR
    # ==================================
    Label(informacion, text="💳 Gestión de Pagos", font=("Arial", 20, "bold"), fg="white", bg=COLOR_FONDO).pack(anchor="w", pady=(10, 20))
    Button(informacion, text="+ Registrar Pago", command=lambda: registrar_pago(informacion, controlador, controlador_clientes), font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", padx=20, pady=8).pack(anchor="w", pady=(0, 20))

    pagos = controlador.obtener_pagos()

    if not pagos:
        Label(informacion, text="No hay pagos registrados", font=("Arial", 13), fg=COLOR_SUBTITULO, bg=COLOR_FONDO).pack(pady=20)
        return

    # ==================================
    # TABLA Y ENCABEZADOS
    # ==================================
    tabla = Frame(informacion, bg=COLOR_PANEL, padx=15, pady=15)
    tabla.pack(fill="x")

    encabezados = ["Cliente", "Membresía", "Monto", "Fecha"]
    for col, texto in enumerate(encabezados):
        Label(tabla, text=texto, font=("Arial", 11, "bold"), fg="white", bg=COLOR_PANEL, padx=15, pady=10).grid(row=0, column=col, sticky="w")

    # ==================================
    # DATOS PAGOS
    # ==================================
    for i, pago in enumerate(pagos):
        fila = i + 1
        Label(tabla, text=pago["cliente"]["nombre"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=0, padx=15, pady=8, sticky="w")
        Label(tabla, text=pago["membresia"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=1, padx=15, pady=8, sticky="w")
        Label(tabla, text=f"${pago['monto']}", font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=2, padx=15, pady=8, sticky="w")
        Label(tabla, text=pago["fecha"], font=("Arial", 11), fg="white", bg=COLOR_PANEL).grid(row=fila, column=3, padx=15, pady=8, sticky="w")


def registrar_pago(informacion, controlador, controlador_clientes):
    ventana_pago = Toplevel()
    ventana_pago.title("Registrar Pago")
    ventana_pago.geometry("550x520")
    ventana_pago.config(bg=COLOR_FONDO)
    ventana_pago.resizable(False, False)

    membresias = [
        {"nombre": "1 Mes", "monto": 12.00},
        {"nombre": "3 Meses", "monto": 34.50},
        {"nombre": "6 Meses", "monto": 66.00},
        {"nombre": "12 Meses", "monto": 126.00},
    ]
    clientes = controlador_clientes.obtener_clientes()

    # ==================================
    # CONTENEDOR Y PANEL FORMULARIO
    # ==================================
    contenedor = Frame(ventana_pago, bg=COLOR_FONDO)
    contenedor.pack(expand=True)

    panel = Frame(contenedor, bg=COLOR_PANEL, padx=40, pady=35)
    panel.pack()

    Label(panel, text="💳 Registrar Pago", font=("Arial", 18, "bold"), fg="white", bg=COLOR_PANEL).pack(pady=(0, 25))

    # Búsqueda de Cliente (Entry + Listbox)
    Label(panel, text="Buscar Cliente", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    entrada_busqueda = Entry(panel, font=FUENTE_INPUT, width=35)
    entrada_busqueda.pack(ipady=7, pady=(5, 10))
    
    lista_clientes = Listbox(panel, height=6, font=("Arial", 11))
    lista_clientes.pack(fill="x", pady=(0, 20))

    def actualizar_lista(*args):
        busqueda = entrada_busqueda.get().lower()
        lista_clientes.delete(0, END)
        for c in clientes:
            if busqueda in c["nombre"].lower() or busqueda in c["cedula"]:
                lista_clientes.insert(END, f"{c['nombre']} | {c['cedula']}")

    actualizar_lista()
    entrada_busqueda.bind("<KeyRelease>", actualizar_lista)

    # Selección de Membresía (OptionMenu)
    Label(panel, text="Membresía", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, anchor="w").pack(fill="x")
    membresia_var = StringVar(ventana_pago, value="1 Mes - $12.0")
    opciones = [f"{m['nombre']} - ${m['monto']}" for m in membresias]
    
    menu = OptionMenu(panel, membresia_var, *opciones)
    menu.config(font=("Arial", 11), width=30)
    menu.pack(pady=(5, 25))

    # ==================================
    # ACCIÓN GUARDAR PAGO
    # ==================================
    def guardar_pago():
        if not lista_clientes.curselection():
            messagebox.showwarning("Error", "Selecciona un cliente")
            return

        seleccion = lista_clientes.get(lista_clientes.curselection())
        cedula = seleccion.split(" | ")[1]
        cliente = next((c for c in clientes if c["cedula"] == cedula), None)

        if cliente.get("membresia"):
            messagebox.showwarning("Aviso", f"{cliente['nombre']} ya tiene una membresía activa")
            return

        opcion = membresia_var.get()
        membresia = next((m for m in membresias if f"{m['nombre']} - ${m['monto']}" == opcion), None)

        controlador.registrar_pago(cliente, membresia, membresia["monto"])
        messagebox.showinfo("Éxito", f"Membresía {membresia['nombre']} asignada a {cliente['nombre']}")
        
        ventana_pago.destroy()
        cargar_pagos(informacion, controlador, controlador_clientes)

    Button(panel, text="REGISTRAR PAGO", command=guardar_pago, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10).pack(fill="x")