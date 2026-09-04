from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from datetime import datetime
from MVC.Controlador.controlador_reservacion import ControladorReservacion
from MVC.Controlador.controlador_rutina import ControladorRutina
from MVC.Vista.estilos import *


def abrir_ventana_usuario(cerrar_ventana, cliente):
    ventana_usuario = Toplevel()
    ventana_usuario.title("Panel Usuario")
    ventana_usuario.geometry("980x650")
    ventana_usuario.config(bg=COLOR_FONDO)

    controlador_reservacion = ControladorReservacion()
    controlador_rutina = ControladorRutina()

    ventana_usuario.protocol("WM_DELETE_WINDOW", lambda: cerrar_ventana(ventana_usuario))

    # ==========================
    # CONTENEDOR PRINCIPAL
    # ==========================
    contenedor = Frame(ventana_usuario, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True)

    # ==========================
    # SIDEBAR
    # ==========================
    navegacion = Frame(contenedor, bg=COLOR_SIDEBAR, width=240)
    navegacion.pack(side="left", fill="y")
    navegacion.pack_propagate(False)

    # ==========================
    # TITULO PANEL
    # ==========================
    Label(navegacion, text="👤 Usuario", font=FUENTE_TITULO_PANEL, fg="white", bg=COLOR_SIDEBAR).pack(pady=(30, 10))
    Label(navegacion, text=f"Bienvenido\n{cliente['nombre']}", font=("Arial", 11), fg=COLOR_SUBTITULO, bg=COLOR_SIDEBAR, justify="center").pack(pady=(0, 30))

    # ==========================
    # CONTENIDO
    # ==========================
    contenido = Frame(contenedor, bg=COLOR_FONDO)
    contenido.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    informacion = Frame(contenido, bg=COLOR_FONDO)
    informacion.pack(fill="both", expand=True)

    # ==========================
    # BOTONES MENU
    # ==========================
    estado_membresia = "normal" if cliente.get("membresia") else "disabled"

    boton_reservaciones = Button(
        navegacion, text="📅 Reservaciones", state=estado_membresia,
        command=lambda: cargar_reservaciones_usuario(informacion, cliente, controlador_reservacion),
        font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10, width=18
    )
    boton_reservaciones.pack(pady=10)

    boton_rutinas = Button(
        navegacion, text="🏋 Mis Rutinas", state=estado_membresia,
        command=lambda: cargar_rutinas_usuario(informacion, cliente, controlador_rutina),
        font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10, width=18
    )
    boton_rutinas.pack(pady=10)

    boton_cuenta = Button(
        navegacion, text="👤 Mi Cuenta", command=lambda: cargar_mi_cuenta(informacion, cliente),
        font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10, width=18
    )
    boton_cuenta.pack(pady=10)

    # ==========================
    # HOVER BOTONES
    # ==========================
    aplicar_hover_boton(boton_reservaciones, COLOR_BOTON, COLOR_BOTON_HOVER)
    aplicar_hover_boton(boton_rutinas, COLOR_BOTON, COLOR_BOTON_HOVER)
    aplicar_hover_boton(boton_cuenta, COLOR_BOTON, COLOR_BOTON_HOVER)

    # ==========================
    # PANTALLA INICIAL
    # ==========================
    Label(informacion, text="🏋 Panel del Usuario", font=FUENTE_TITULO_PANEL, fg="white", bg=COLOR_FONDO).pack(pady=(40, 10))
    Label(informacion, text="Selecciona una opción del menú", font=("Arial", 12), fg=COLOR_SUBTITULO, bg=COLOR_FONDO).pack()


def limpiar(informacion):
    for widget in informacion.winfo_children():
        widget.destroy()


def cargar_mi_cuenta(informacion, cliente):
    limpiar(informacion)

    contenedor = Frame(informacion, bg=COLOR_FONDO)
    contenedor.pack(fill="both", expand=True, padx=30, pady=25)

    Label(contenedor, text="👤 Mi Cuenta", font=FUENTE_TITULO_PANEL, fg="white", bg=COLOR_FONDO).pack(anchor="w", pady=(0, 20))

    tarjeta = Frame(contenedor, bg=COLOR_PANEL, padx=35, pady=30)
    tarjeta.pack(fill="x")

    # Nombre
    Label(tarjeta, text="Nombre", font=FUENTE_LABEL, fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w")
    Label(tarjeta, text=cliente["nombre"], font=("Arial", 15, "bold"), fg="white", bg=COLOR_PANEL).pack(anchor="w", pady=(0, 18))

    # Cédula
    Label(tarjeta, text="Cédula", font=FUENTE_LABEL, fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w")
    Label(tarjeta, text=cliente["cedula"], font=("Arial", 15, "bold"), fg="white", bg=COLOR_PANEL).pack(anchor="w", pady=(0, 18))

    # Teléfono
    Label(tarjeta, text="Teléfono", font=FUENTE_LABEL, fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w")
    Label(tarjeta, text=cliente["telefono"], font=("Arial", 15, "bold"), fg="white", bg=COLOR_PANEL).pack(anchor="w", pady=(0, 18))

    # Membresía
    Label(tarjeta, text="Membresía", font=FUENTE_LABEL, fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w")
    membresia = cliente["membresia"] if cliente.get("membresia") else "Sin membresía"
    color_membresia = "#22c55e" if cliente.get("membresia") else "#ef4444"
    Label(tarjeta, text=membresia, font=("Arial", 15, "bold"), fg=color_membresia, bg=COLOR_PANEL).pack(anchor="w")


def cargar_reservaciones_usuario(informacion, cliente, controlador):
    limpiar(informacion)
    frame_scroll = crear_frame_scroll(informacion)

    Label(frame_scroll, text="📅 Mis Reservaciones", font=FUENTE_TITULO_PANEL, fg="white", bg=COLOR_FONDO).pack(anchor="w", pady=(10, 20), padx=20)

    boton_nueva = Button(
        frame_scroll, text="➕ Nueva Reservación", command=lambda: agregar_reservacion_usuario(informacion, cliente, controlador),
        font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", relief="flat", cursor="hand2", pady=10
    )
    boton_nueva.pack(anchor="w", padx=20, pady=(0, 20))
    aplicar_hover_boton(boton_nueva, COLOR_BOTON, COLOR_BOTON_HOVER)

    reservaciones = controlador.obtener_reservaciones_cliente(cliente)

    if not reservaciones:
        tarjeta_vacia = Frame(frame_scroll, bg=COLOR_PANEL, padx=30, pady=25)
        tarjeta_vacia.pack(fill="x", padx=20)
        Label(tarjeta_vacia, text="No tienes reservaciones", font=("Arial", 14), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack()
        return

    for reservacion in reservaciones:
        tarjeta = Frame(frame_scroll, bg=COLOR_PANEL, padx=20, pady=20)
        tarjeta.pack(fill="x", padx=20, pady=10)

        Label(tarjeta, text=f"🏟 {reservacion['cancha']}", font=("Arial", 16, "bold"), fg="white", bg=COLOR_PANEL).pack(anchor="w")
        Label(tarjeta, text=f"📅 Fecha: {reservacion['fecha']}", font=("Arial", 12), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w", pady=(10, 0))
        Label(tarjeta, text=f"⏰ Hora: {reservacion['hora']}", font=("Arial", 12), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w")

        estado_color = "#22c55e" if reservacion["estado"] == "activa" else "#ef4444"
        Label(tarjeta, text=f"Estado: {reservacion['estado'].capitalize()}", font=("Arial", 12, "bold"), fg=estado_color, bg=COLOR_PANEL).pack(anchor="w", pady=(5, 15))

        if reservacion["estado"] == "activa":
            boton_cancelar = Button(
                tarjeta, text="❌ Cancelar Reservación", command=lambda r=reservacion: cancelar_reservacion_usuario(r, informacion, cliente, controlador),
                font=FUENTE_BOTON, bg="#dc2626", fg="white", relief="flat", cursor="hand2", pady=8
            )
            boton_cancelar.pack(anchor="e")
            aplicar_hover_boton(boton_cancelar, "#dc2626", "#b91c1c")


def agregar_reservacion_usuario(informacion, cliente, controlador):
    from MVC.Controlador.controlador_rutina import ControladorRutina

    ventana_reservacion = Toplevel()
    ventana_reservacion.title("Nueva Reservacion")
    ventana_reservacion.geometry("400x500")

    controlador_rutina = ControladorRutina()
    hoy = datetime.now()
    max_fecha = hoy + __import__('datetime').timedelta(days=30)

    # ── Cancha ──
    Label(ventana_reservacion, text="Cancha").grid(row=0, column=0)
    cancha_var = StringVar(ventana_reservacion, value="Futbol")
    OptionMenu(ventana_reservacion, cancha_var, "Futbol", "Voleibol", "Baloncesto", "Gimnasio", "Piscina").grid(row=0, column=1)

    # ── Objetivo ──
    Label(ventana_reservacion, text="Objetivo").grid(row=1, column=0)
    objetivo_var = StringVar(ventana_reservacion, value="Resistencia")
    menu_objetivo = OptionMenu(ventana_reservacion, objetivo_var, "Resistencia")
    menu_objetivo.grid(row=1, column=1)

    def actualizar_objetivos(*args):
        objetivos = controlador_rutina.obtener_objetivos(cancha_var.get())
        objetivos.append("El entrenador decide")
        menu_objetivo["menu"].delete(0, "end")
        for obj in objetivos:
            menu_objetivo["menu"].add_command(label=obj, command=lambda o=obj: objetivo_var.set(o))
        objetivo_var.set(objetivos[0])

    cancha_var.trace("w", actualizar_objetivos)
    actualizar_objetivos()

    # ── Calendario ──
    Label(ventana_reservacion, text="Fecha").grid(row=2, column=0)
    calendario = Calendar(ventana_reservacion, selectmode="day", year=hoy.year, month=hoy.month, day=hoy.day, mindate=hoy.date(), maxdate=max_fecha.date())
    calendario.grid(row=2, column=1)

    # ── Hora ──
    Label(ventana_reservacion, text="Hora").grid(row=3, column=0)
    hora_var = StringVar(ventana_reservacion, value="06:00")
    menu_hora = OptionMenu(ventana_reservacion, hora_var, "06:00")
    menu_hora.grid(row=3, column=1)

    def actualizar_horas(*args):
        fecha = datetime.strptime(calendario.get_date(), "%m/%d/%y").date()
        ahora = datetime.now()
        horas_disponibles = []
        for h in range(6, 23):
            hora_str = f"{h:02d}:00"
            if fecha != ahora.date() or h > ahora.hour:
                horas_disponibles.append(hora_str)

        menu_hora["menu"].delete(0, "end")
        for hora in horas_disponibles:
            menu_hora["menu"].add_command(label=hora, command=lambda h=hora: hora_var.set(h))
        hora_var.set(horas_disponibles[0] if horas_disponibles else "No hay horas disponibles")

    calendario.bind("<<CalendarSelected>>", actualizar_horas)
    actualizar_horas()

    def guardar_reservacion():
        fecha = datetime.strptime(calendario.get_date(), "%m/%d/%y").strftime("%Y-%m-%d")
        hora = hora_var.get()

        if hora == "No hay horas disponibles":
            messagebox.showwarning("Error", "No hay horas disponibles para hoy")
            return

        if any(r["fecha"] == fecha and r["hora"] == hora and r["estado"] == "activa" for r in controlador.obtener_reservaciones_cliente(cliente)):
            messagebox.showwarning("Error", "El cliente ya tiene una reservación en esa fecha y hora")
            return

        if not controlador.verificar_disponibilidad(cancha_var.get(), fecha, hora):
            messagebox.showerror("Error", "La cancha no está disponible en ese horario")
            return

        controlador.agregar_reservacion({
            "cliente": cliente, "cancha": cancha_var.get(), "objetivo": objetivo_var.get(),
            "fecha": fecha, "hora": hora, "estado": "activa"
        })
        ventana_reservacion.destroy()
        cargar_reservaciones_usuario(informacion, cliente, controlador)

    Button(ventana_reservacion, text="Guardar", command=guardar_reservacion).grid(row=4, column=0, columnspan=2)


def cancelar_reservacion_usuario(reservacion, informacion, cliente, controlador):
    if messagebox.askyesno("Confirmar cancelación", "¿Seguro que deseas cancelar esta reservación?"):
        controlador.cancelar_reservacion(reservacion)
        cargar_reservaciones_usuario(informacion, cliente, controlador)


def cargar_rutinas_usuario(informacion, cliente, controlador):
    limpiar(informacion)
    frame_scroll = crear_frame_scroll(informacion)

    Label(frame_scroll, text="🏋 Mis Rutinas", font=FUENTE_TITULO_PANEL, fg="white", bg=COLOR_FONDO).pack(anchor="w", padx=20, pady=(10, 20))

    rutina_hoy = controlador.obtener_rutina_hoy(cliente)

    if rutina_hoy:
        tarjeta_hoy = Frame(frame_scroll, bg=COLOR_PANEL, padx=20, pady=20)
        tarjeta_hoy.pack(fill="x", padx=20, pady=(0, 20))

        Label(tarjeta_hoy, text="🔥 Rutina de Hoy", font=("Arial", 16, "bold"), fg="white", bg=COLOR_PANEL).pack(anchor="w")
        Label(tarjeta_hoy, text=f"🏟 {rutina_hoy['cancha']}", font=("Arial", 13, "bold"), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w", pady=(10, 0))
        Label(tarjeta_hoy, text=f"🎯 Objetivo: {rutina_hoy['objetivo']}", font=("Arial", 12), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w", pady=(5, 15))

        tabla = Frame(tarjeta_hoy, bg=COLOR_PANEL)
        tabla.pack(fill="x")

        for col, texto in enumerate(["Ejercicio", "Series", "Repeticiones"]):
            Label(tabla, text=texto, font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL, padx=20, pady=10).grid(row=0, column=col, sticky="w")

        for i, ejercicio in enumerate(rutina_hoy["ejercicios"]):
            fila_bg = COLOR_PANEL if i % 2 == 0 else "#263449"
            Label(tabla, text=ejercicio["nombre"], bg=fila_bg, fg="white", padx=20, pady=10).grid(row=i + 1, column=0, sticky="w")
            Label(tabla, text=ejercicio["series"], bg=fila_bg, fg="white", padx=20).grid(row=i + 1, column=1, sticky="w")
            Label(tabla, text=ejercicio["repeticiones"], bg=fila_bg, fg="white", padx=20).grid(row=i + 1, column=2, sticky="w")
    else:
        tarjeta_vacia = Frame(frame_scroll, bg=COLOR_PANEL, padx=30, pady=25)
        tarjeta_vacia.pack(fill="x", padx=20, pady=(0, 20))
        Label(tarjeta_vacia, text="No tienes rutina asignada para hoy", font=("Arial", 14), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack()

    anteriores = [r for r in controlador.obtener_rutinas_cliente(cliente) if r != rutina_hoy]

    if anteriores:
        Label(frame_scroll, text="📋 Rutinas Anteriores", font=FUENTE_TITULO_PANEL, fg="white", bg=COLOR_FONDO).pack(anchor="w", padx=20, pady=(10, 15))

        for rutina in reversed(anteriores):
            tarjeta = Frame(frame_scroll, bg=COLOR_PANEL, padx=20, pady=20)
            tarjeta.pack(fill="x", padx=20, pady=10)

            Label(tarjeta, text=f"📅 {rutina['fecha']}", font=("Arial", 14, "bold"), fg="white", bg=COLOR_PANEL).pack(anchor="w")
            Label(tarjeta, text=f"🏟 {rutina['cancha']}", font=("Arial", 12), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w", pady=(8, 0))
            Label(tarjeta, text=f"🎯 Objetivo: {rutina['objetivo']}", font=("Arial", 12), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w", pady=(3, 10))
            Label(tarjeta, text="Ejercicios:", font=FUENTE_LABEL, fg="white", bg=COLOR_PANEL).pack(anchor="w")

            for ej in rutina["ejercicios"]:
                texto_ej = f"• {ej['nombre']} — {ej['series']} series x {ej['repeticiones']} reps"
                Label(tarjeta, text=texto_ej, font=("Arial", 11), fg=COLOR_SUBTITULO, bg=COLOR_PANEL).pack(anchor="w", pady=2)