from tkinter import *
from tkinter import messagebox
from datetime import datetime
from MVC.Controlador.controlador_rutina import ControladorRutina
from MVC.Controlador.controlador_reservacion import ControladorReservacion
from MVC.Vista.estilos import *


def abrir_ventana_entrenador(cerrar_ventana, entrenador):

    ventana_entrenador = Toplevel()
    ventana_entrenador.title("Panel Entrenador")
    ventana_entrenador.geometry("980x650")
    ventana_entrenador.config(bg=COLOR_FONDO)

    controlador_rutina = ControladorRutina()

    ventana_entrenador.protocol(
        "WM_DELETE_WINDOW",
        lambda: cerrar_ventana(ventana_entrenador)
    )

    # ==========================
    # CONTENEDOR PRINCIPAL
    # ==========================

    contenedor = Frame(ventana_entrenador, bg=COLOR_FONDO)
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

    Label(
        navegacion,
        text="🏋 Entrenador",
        font=("Arial", 18, "bold"),
        fg="white",
        bg=COLOR_SIDEBAR
    ).pack(pady=(30, 10))

    Label(
        navegacion,
        text=f"Bienvenido\n{entrenador['nombre']}",
        font=("Arial", 11),
        fg="#cbd5e1",
        bg=COLOR_SIDEBAR,
        justify="center"
    ).pack(pady=(0, 30))

    # ==========================
    # AREA CONTENIDO
    # ==========================

    contenido = Frame(contenedor, bg=COLOR_FONDO)
    contenido.pack(side="right", fill="both", expand=True, padx=20, pady=20)

    # ==========================
    # CONTENIDO SCROLLABLE
    # ==========================

    informacion_container = Frame(contenido, bg=COLOR_FONDO)
    informacion_container.pack(fill="both", expand=True)

    informacion = crear_frame_scroll(informacion_container)

    # ==========================
    # BOTONES MENU
    # ==========================

    boton_alumnos = Button(
        navegacion,
        text="👥 Mis Alumnos",
        command=lambda: cargar_alumnos(informacion, entrenador, controlador_rutina),
        font=FUENTE_BOTON,
        bg=COLOR_BOTON,
        fg="white",
        relief="flat",
        cursor="hand2",
        pady=10,
        width=18
    )
    boton_alumnos.pack(pady=10)

    boton_rutinas = Button(
        navegacion,
        text="📋 Mis Rutinas",
        command=lambda: cargar_rutinas_entrenador(informacion, entrenador, controlador_rutina),
        font=FUENTE_BOTON,
        bg=COLOR_BOTON,
        fg="white",
        relief="flat",
        cursor="hand2",
        pady=10,
        width=18
    )
    boton_rutinas.pack(pady=10)

    # ==========================
    # HOVER BOTONES
    # ==========================

    aplicar_hover_boton(boton_alumnos, COLOR_BOTON, "#15803d")
    aplicar_hover_boton(boton_rutinas, COLOR_BOTON, "#15803d")

    # ==========================
    # PANTALLA INICIAL
    # ==========================

    Label(
        informacion,
        text="🏋 Panel del Entrenador",
        font=("Arial", 20, "bold"),
        fg="white",
        bg=COLOR_FONDO
    ).pack(pady=(40, 10))

    Label(
        informacion,
        text="Selecciona una opción del menú",
        font=("Arial", 12),
        fg=COLOR_SUBTITULO,
        bg=COLOR_FONDO
    ).pack()


def limpiar(informacion):
    for widget in informacion.winfo_children():
        widget.destroy()


def cargar_alumnos(informacion, entrenador, controlador_rutina):
    limpiar(informacion)

    # ==========================
    # TITULO
    # ==========================

    Label(
        informacion,
        text="👥 Mis Alumnos",
        font=FUENTE_TITULO_PANEL,
        fg="white",
        bg=COLOR_FONDO
    ).pack(anchor="w", pady=(10, 20))

    # ==========================
    # OBTENER RESERVACIONES DESDE POSTGRESQL
    # ==========================

    controlador_reservacion = ControladorReservacion()
    todas = controlador_reservacion.obtener_reservaciones()

    hoy = datetime.now().strftime("%Y-%m-%d")
    alumnos_hoy = [
        r for r in todas
        if r["cancha"] == entrenador["especialidad"]
        and r["fecha"] == hoy
        and r["estado"] == "activa"
    ]

    if not alumnos_hoy:
        Label(
            informacion,
            text="No hay alumnos programados para hoy",
            font=FUENTE_SUBTITULO,
            fg=COLOR_SUBTITULO,
            bg=COLOR_FONDO
        ).pack(pady=30)
        return

    # ==========================
    # PANEL TABLA
    # ==========================

    panel = Frame(informacion, bg=COLOR_PANEL, padx=20, pady=20)
    panel.pack(fill="x")

    # ==========================
    # ENCABEZADOS
    # ==========================

    encabezados = ["Cliente", "Objetivo", "Rutina", "Acción"]
    for col, texto in enumerate(encabezados):
        Label(
            panel,
            text=texto,
            font=FUENTE_LABEL,
            fg="white",
            bg=COLOR_PANEL,
            padx=20,
            pady=10
        ).grid(row=0, column=col, sticky="w")

    # ==========================
    # FILAS
    # ==========================

    for i, reservacion in enumerate(alumnos_hoy):
        cliente = reservacion["cliente"]
        objetivo = reservacion.get("objetivo", "El entrenador decide")

        rutina_hoy = controlador_rutina.obtener_rutina_reservacion(
            cliente,
            reservacion["fecha"],
            reservacion["hora"]
        )
        tiene_rutina = "✅" if rutina_hoy else "❌"
        fila_bg = COLOR_PANEL if i % 2 == 0 else "#263449"

        Label(
            panel,
            text=cliente["nombre"],
            bg=fila_bg,
            fg="white",
            padx=20,
            pady=12
        ).grid(row=i + 1, column=0, sticky="w")

        Label(
            panel,
            text=objetivo,
            bg=fila_bg,
            fg="white",
            padx=20
        ).grid(row=i + 1, column=1, sticky="w")

        Label(
            panel,
            text=tiene_rutina,
            bg=fila_bg,
            fg="white",
            padx=20
        ).grid(row=i + 1, column=2, sticky="w")

        if not rutina_hoy:
            boton_asignar = Button(
                panel,
                text="Asignar",
                command=lambda r=reservacion: asignar_rutina(
                    r, entrenador, informacion, controlador_rutina
                ),
                bg=COLOR_BOTON,
                fg="white",
                relief="flat",
                cursor="hand2",
                font=FUENTE_BOTON
            )
            boton_asignar.grid(row=i + 1, column=3, padx=10, pady=5)
            aplicar_hover_boton(boton_asignar)


def validar_numero_positivo(valor):

    if valor == "":
        return True

    if not valor.isdigit():
        return False

    numero = int(valor)

    if numero < 0:
        return False

    if numero > 999:
        return False

    return True


def asignar_rutina(reservacion, entrenador, informacion, controlador_rutina):
    cliente = reservacion["cliente"]
    cancha  = reservacion["cancha"]
    objetivo = reservacion.get("objetivo", "El entrenador decide")

    ventana_rutina = Toplevel()
    ventana_rutina.title("Asignar Rutina")
    ventana_rutina.geometry("760x650")
    ventana_rutina.config(bg=COLOR_FONDO)

    # ==========================
    # PANEL PRINCIPAL
    # ==========================

    panel = Frame(ventana_rutina, bg=COLOR_PANEL, padx=30, pady=25)
    panel.pack(fill="both", expand=True, padx=20, pady=20)

    # ==========================
    # TITULO
    # ==========================

    Label(
        panel,
        text="🏋 Asignar Rutina",
        font=FUENTE_TITULO_PANEL,
        bg=COLOR_PANEL,
        fg="white"
    ).pack(pady=(0, 20))

    # ==========================
    # INFO CLIENTE
    # ==========================

    info_frame = Frame(panel, bg=COLOR_PANEL)
    info_frame.pack(fill="x", pady=(0, 20))

    Label(
        info_frame,
        text=f"Cliente: {cliente['nombre']}",
        font=FUENTE_LABEL,
        fg="white",
        bg=COLOR_PANEL
    ).pack(anchor="w")

    Label(
        info_frame,
        text=f"Cancha: {cancha}",
        font=FUENTE_LABEL,
        fg="white",
        bg=COLOR_PANEL
    ).pack(anchor="w", pady=5)

    # ==========================
    # OBJETIVO
    # ==========================

    Label(
        panel,
        text="Objetivo",
        font=FUENTE_LABEL,
        bg=COLOR_PANEL,
        fg="white"
    ).pack(anchor="w")

    objetivo_var = StringVar(ventana_rutina)

    if objetivo == "El entrenador decide":
        objetivos = controlador_rutina.obtener_objetivos(cancha)
        objetivo_var.set(objetivos[0])
        menu_objetivo = OptionMenu(panel, objetivo_var, *objetivos)
        estilizar_optionmenu(menu_objetivo)
        menu_objetivo.pack(anchor="w", pady=(5, 20))
    else:
        objetivo_var.set(objetivo)
        Label(
            panel,
            text=objetivo,
            bg=COLOR_PANEL,
            fg="white"
        ).pack(anchor="w", pady=(5, 20))

    # ==========================
    # TABLA EJERCICIOS
    # ==========================

    Label(
        panel,
        text="Ejercicios",
        font=FUENTE_LABEL,
        bg=COLOR_PANEL,
        fg="white"
    ).pack(anchor="w")

    frame_ejercicios = Frame(panel, bg=COLOR_PANEL)
    frame_ejercicios.pack(fill="x", pady=15)

    entradas_ejercicios = []

    validacion = ventana_rutina.register(validar_numero_positivo)

    def cargar_ejercicios(*args):
        for widget in frame_ejercicios.winfo_children():
            widget.destroy()
        entradas_ejercicios.clear()

        ejercicios = controlador_rutina.obtener_ejercicios(cancha, objetivo_var.get())
        encabezados = ["Ejercicio", "Series", "Reps"]

        for col, texto in enumerate(encabezados):
            Label(
                frame_ejercicios,
                text=texto,
                font=FUENTE_LABEL,
                bg=COLOR_PANEL,
                fg="white",
                padx=20
            ).grid(row=0, column=col, pady=10)

        for j, ejercicio in enumerate(ejercicios):
            fila_bg = COLOR_PANEL if j % 2 == 0 else "#263449"

            Label(
                frame_ejercicios,
                text=ejercicio,
                bg=fila_bg,
                fg="white",
                width=25,
                anchor="w",
                padx=10,
                pady=8
            ).grid(row=j + 1, column=0, sticky="ew")

            entrada_series = Entry(
                frame_ejercicios,
                width=8,
                font=FUENTE_INPUT,
                justify="center",
                validate="key",
                validatecommand=(validacion, "%P")
            )
            entrada_series.insert(0, "3")
            entrada_series.grid(row=j + 1, column=1, padx=10)

            entrada_reps = Entry(
                frame_ejercicios,
                width=8,
                font=FUENTE_INPUT,
                justify="center",
                validate="key",
                validatecommand=(validacion, "%P")
            )
            entrada_reps.insert(0, "12")
            entrada_reps.grid(row=j + 1, column=2, padx=10)

            entradas_ejercicios.append((ejercicio, entrada_series, entrada_reps))

    objetivo_var.trace("w", cargar_ejercicios)
    cargar_ejercicios()

    # ==========================
    # GUARDAR
    # ==========================

    def guardar_rutina():

        ejercicios = []

        for nombre, entrada_series, entrada_reps in entradas_ejercicios:

            try:
                texto_series = entrada_series.get().strip()
                texto_reps   = entrada_reps.get().strip()

                if texto_series == "" or texto_reps == "":
                    messagebox.showerror(
                        "Error",
                        f"Completa series y repeticiones en '{nombre}'"
                    )
                    return

                series = int(texto_series)
                reps   = int(texto_reps)

            except ValueError:
                messagebox.showerror(
                    "Error",
                    f"'{nombre}' debe tener números válidos"
                )
                return

            if series < 0 or reps < 0:
                messagebox.showerror(
                    "Error",
                    f"'{nombre}' no puede tener valores negativos"
                )
                return

            if (series == 0 and reps > 0) or (series > 0 and reps == 0):
                messagebox.showerror(
                    "Error",
                    f"En '{nombre}' ambas deben ser mayores a 0 o ambas 0"
                )
                return

            if series > 20:
                messagebox.showerror(
                    "Error",
                    f"'{nombre}' tiene demasiadas series (máximo 20)"
                )
                return

            if reps > 100:
                messagebox.showerror(
                    "Error",
                    f"'{nombre}' tiene demasiadas repeticiones (máximo 100)"
                )
                return

            if series == 0 and reps == 0:
                continue

            ejercicios.append({
                "nombre":       nombre,
                "series":       series,
                "repeticiones": reps
            })

        if not ejercicios:
            messagebox.showerror(
                "Error",
                "Debes asignar al menos un ejercicio"
            )
            return

        controlador_rutina.agregar_rutina(
            cliente,
            entrenador,
            cancha,
            objetivo_var.get(),
            ejercicios,
            reservacion["fecha"],
            reservacion["hora"]
        )

        ventana_rutina.destroy()

        informacion.after(
            100,
            lambda: cargar_alumnos(informacion, entrenador, controlador_rutina)
        )

        messagebox.showinfo(
            "Éxito",
            f"Rutina asignada a {cliente['nombre']}"
        )

    # ==========================
    # BOTON GUARDAR
    # ==========================

    boton_guardar = Button(
        panel,
        text="Guardar Rutina",
        command=guardar_rutina,
        bg=COLOR_BOTON,
        fg="white",
        relief="flat",
        cursor="hand2",
        font=FUENTE_BOTON,
        pady=10
    )
    boton_guardar.pack(pady=20)
    aplicar_hover_boton(boton_guardar)


def cargar_rutinas_entrenador(informacion, entrenador, controlador_rutina):
    limpiar(informacion)

    Label(
        informacion,
        text="📋 Mis Rutinas",
        font=FUENTE_TITULO_PANEL,
        fg="white",
        bg=COLOR_FONDO
    ).pack(anchor="w", pady=(10, 20))

    todas = controlador_rutina.obtener_rutinas()
    mis_rutinas = [
        r for r in todas
        if r["entrenador"]["cedula"] == entrenador["cedula"]
    ]

    if not mis_rutinas:
        Label(
            informacion,
            text="No has asignado rutinas aún",
            font=FUENTE_SUBTITULO,
            fg=COLOR_SUBTITULO,
            bg=COLOR_FONDO
        ).pack(pady=40)
        return

    # ==========================
    # TARJETAS DE RUTINAS
    # ==========================

    for rutina in mis_rutinas:
        tarjeta = Frame(informacion, bg=COLOR_PANEL, padx=20, pady=20)
        tarjeta.pack(fill="x", pady=10)

        Label(
            tarjeta,
            text=f"👤 Cliente: {rutina['cliente']['nombre']}",
            font=FUENTE_LABEL,
            fg="white",
            bg=COLOR_PANEL
        ).pack(anchor="w")

        Label(
            tarjeta,
            text=f"🎯 Objetivo: {rutina['objetivo']}",
            fg=COLOR_SUBTITULO,
            bg=COLOR_PANEL,
            font=FUENTE_SUBTITULO
        ).pack(anchor="w", pady=(5, 0))

        Label(
            tarjeta,
            text=f"📅 Fecha: {rutina['fecha']}",
            fg=COLOR_SUBTITULO,
            bg=COLOR_PANEL,
            font=FUENTE_SUBTITULO
        ).pack(anchor="w", pady=(5, 15))

        Label(
            tarjeta,
            text="🏋 Ejercicios Asignados",
            font=FUENTE_LABEL,
            fg="white",
            bg=COLOR_PANEL
        ).pack(anchor="w", pady=(0, 10))

        tabla = Frame(tarjeta, bg=COLOR_PANEL)
        tabla.pack(fill="x")

        encabezados = ["Ejercicio", "Series", "Repeticiones"]
        for col, texto in enumerate(encabezados):
            Label(
                tabla,
                text=texto,
                font=FUENTE_LABEL,
                fg="white",
                bg=COLOR_PANEL,
                padx=20,
                pady=8
            ).grid(row=0, column=col, sticky="w")

        for i, ejercicio in enumerate(rutina["ejercicios"]):
            fila_bg = COLOR_PANEL if i % 2 == 0 else "#263449"

            Label(
                tabla,
                text=ejercicio["nombre"],
                bg=fila_bg,
                fg="white",
                padx=20,
                pady=8
            ).grid(row=i + 1, column=0, sticky="w")

            Label(
                tabla,
                text=ejercicio["series"],
                bg=fila_bg,
                fg="white",
                padx=20
            ).grid(row=i + 1, column=1, sticky="w")

            Label(
                tabla,
                text=ejercicio["repeticiones"],
                bg=fila_bg,
                fg="white",
                padx=20
            ).grid(row=i + 1, column=2, sticky="w")