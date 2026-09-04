from Database.conexion import ejecutar


class ModeloCancha:

    def obtener_canchas(self):
        return ejecutar(
            """
            SELECT esc_nombre           AS sector,
                   esc_capacidad        AS capacidad,
                   esc_ocupacion_actual AS ocupacion_actual,
                   esc_activo           AS activo
            FROM escenario
            ORDER BY esc_nombre
            """,
            fetchall=True
        )

    def cambiar_estado(self, cancha):
        ejecutar(
            """
            UPDATE escenario
            SET esc_activo = NOT esc_activo
            WHERE esc_nombre = %s
            """,
            (cancha["sector"],)
        )
        # Reflejar el cambio en el dict para que la vista
        # no necesite recargar desde BD
        cancha["activo"] = not cancha["activo"]
