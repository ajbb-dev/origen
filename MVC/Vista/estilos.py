from tkinter import *

# ==========================
# COLORES
# ==========================

COLOR_FONDO = "#0f172a"
COLOR_PANEL = "#1e293b"
COLOR_SIDEBAR = "#172033"

COLOR_TEXTO = "white"
COLOR_SUBTITULO = "#cbd5e1"

COLOR_BOTON = "#22c55e"
COLOR_BOTON_HOVER = "#16a34a"

# ==========================
# FUENTES
# ==========================

FUENTE_TITULO = (
    "Arial",
    22,
    "bold"
)

FUENTE_TITULO_PANEL = (
    "Arial",
    18,
    "bold"
)

FUENTE_SUBTITULO = (
    "Arial",
    14
)

FUENTE_LABEL = (
    "Arial",
    11,
    "bold"
)

FUENTE_INPUT = (
    "Arial",
    12
)

FUENTE_BOTON = (
    "Arial",
    12,
    "bold"
)

# ==========================
# CONFIG INPUTS
# ==========================

ANCHO_INPUT = 30

# ==========================
# HOVER BOTONES
# ==========================

def aplicar_hover_boton(
    boton,
    color_normal=COLOR_BOTON,
    color_hover=COLOR_BOTON_HOVER
):

    boton.bind(
        "<Enter>",
        lambda e:
        boton.config(
            bg=color_hover
        )
    )

    boton.bind(
        "<Leave>",
        lambda e:
        boton.config(
            bg=color_normal
        )
    )


# ==========================
# OPTION MENU BONITO
# ==========================

def estilizar_optionmenu(menu):

    menu.config(
        font=("Arial", 11),
        width=24,
        bg=COLOR_PANEL,
        fg="white",
        activebackground="#2563eb",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        highlightthickness=0
    )

    menu["menu"].config(
        bg=COLOR_PANEL,
        fg="white",
        font=("Arial", 10),
        activebackground="#2563eb",
        activeforeground="white"
    )


# ==========================
# FRAME CON SCROLL
# ==========================

def crear_frame_scroll(parent):

    # ==========================
    # CONTENEDOR
    # ==========================

    contenedor = Frame(
        parent,
        bg=COLOR_FONDO
    )

    contenedor.pack(
        fill="both",
        expand=True
    )

    # ==========================
    # CANVAS
    # ==========================

    canvas = Canvas(
        contenedor,
        bg=COLOR_FONDO,
        highlightthickness=0,
        bd=0
    )

    scrollbar = Scrollbar(
        contenedor,
        orient="vertical",
        command=canvas.yview
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    # ==========================
    # FRAME INTERNO
    # ==========================

    frame_scroll = Frame(
        canvas,
        bg=COLOR_FONDO
    )

    ventana_canvas = canvas.create_window(
        (0, 0),
        window=frame_scroll,
        anchor="nw"
    )

    # ==========================
    # ACTUALIZAR SCROLL
    # ==========================

    def actualizar_scroll(event=None):

        canvas.configure(
            scrollregion=canvas.bbox("all")
        )

    frame_scroll.bind(
        "<Configure>",
        actualizar_scroll
    )

    # ==========================
    # AJUSTAR ANCHO
    # ==========================

    def ajustar_ancho(event):

        canvas.itemconfig(
            ventana_canvas,
            width=event.width
        )

    canvas.bind(
        "<Configure>",
        ajustar_ancho
    )

    # ==========================
    # SCROLL WINDOWS
    # ==========================

    def scroll_mouse(event):

        posicion = canvas.yview()

        # Ya está arriba
        if event.delta > 0:

            if posicion[0] <= 0:
                return

        # Ya está abajo
        elif event.delta < 0:

            if posicion[1] >= 1:
                return

        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        scroll_mouse
    )

    # ==========================
    # SCROLL LINUX
    # ==========================

    def scroll_linux_up(event):

        if canvas.yview()[0] > 0:

            canvas.yview_scroll(
                -1,
                "units"
            )

    def scroll_linux_down(event):

        if canvas.yview()[1] < 1:

            canvas.yview_scroll(
                1,
                "units"
            )

    canvas.bind_all(
        "<Button-4>",
        scroll_linux_up
    )

    canvas.bind_all(
        "<Button-5>",
        scroll_linux_down
    )

    # ==========================
    # POSICIÓN INICIAL
    # ==========================

    canvas.after(
        50,
        lambda:
        canvas.yview_moveto(0)
    )

    # ==========================
    # PACK
    # ==========================

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    return frame_scroll