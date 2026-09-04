from Database.conexion import ejecutar


class ModeloReservacion:

    def obtener_reservaciones(self):
        rows = ejecutar(
            """
            SELECT
                res_id                  AS id,
                res_nombre_escenario    AS cancha,
                res_objetivo            AS objetivo,
                res_fecha::text         AS fecha,
                res_hora                AS hora,
                res_estado              AS estado,
                cli_cedula              AS cliente_cedula,
                cli_nombre              AS cliente_nombre,
                cli_telefono            AS cliente_telefono,
                cli_membresia           AS cliente_membresia
            FROM reservacion
            JOIN cliente ON cli_cedula = res_cedula_cliente
            ORDER BY res_fecha DESC, res_hora
            """,
            fetchall=True
        )
        return [self._formatear(r) for r in rows]

    def obtener_reservaciones_cliente(self, cliente):
        rows = ejecutar(
            """
            SELECT
                res_id                  AS id,
                res_nombre_escenario    AS cancha,
                res_objetivo            AS objetivo,
                res_fecha::text         AS fecha,
                res_hora                AS hora,
                res_estado              AS estado,
                cli_cedula              AS cliente_cedula,
                cli_nombre              AS cliente_nombre,
                cli_telefono            AS cliente_telefono,
                cli_membresia           AS cliente_membresia
            FROM reservacion
            JOIN cliente ON cli_cedula = res_cedula_cliente
            WHERE res_cedula_cliente = %s
            ORDER BY res_fecha DESC, res_hora
            """,
            (cliente["cedula"],),
            fetchall=True
        )
        return [self._formatear(r) for r in rows]

    def agregar_reservacion(self, reservacion):
        ejecutar(
            """
            INSERT INTO reservacion
                (res_cedula_cliente, res_nombre_escenario,
                 res_objetivo, res_fecha, res_hora, res_estado)
            VALUES (%s, %s, %s, %s, %s, 'activa')
            """,
            (
                reservacion["cliente"]["cedula"],
                reservacion["cancha"],
                reservacion["objetivo"],
                reservacion["fecha"],
                reservacion["hora"]
            )
        )

        ejecutar(
            """
            UPDATE escenario
            SET esc_ocupacion_actual = esc_ocupacion_actual + 1
            WHERE esc_nombre = %s
            """,
            (reservacion["cancha"],)
        )

    def cancelar_reservacion(self, reservacion):
        ejecutar(
            """
            UPDATE reservacion
            SET res_estado = 'cancelada'
            WHERE res_id = %s
            """,
            (reservacion["id"],)
        )

        ejecutar(
            """
            UPDATE escenario
            SET esc_ocupacion_actual = GREATEST(esc_ocupacion_actual - 1, 0)
            WHERE esc_nombre = %s
            """,
            (reservacion["cancha"],)
        )

        reservacion["estado"] = "cancelada"

    def verificar_disponibilidad(self, cancha, fecha, hora):

        conteo = ejecutar(
            """
            SELECT COUNT(*) AS total
            FROM reservacion
            WHERE res_nombre_escenario = %s
              AND res_fecha = %s
              AND res_hora  = %s
              AND res_estado = 'activa'
            """,
            (cancha, fecha, hora),
            fetchone=True
        )

        escenario = ejecutar(
            """
            SELECT esc_capacidad AS capacidad,
                   esc_activo    AS activo
            FROM escenario
            WHERE esc_nombre = %s
            """,
            (cancha,),
            fetchone=True
        )

        if not escenario:
            return False

        return (
            int(conteo["total"]) < escenario["capacidad"]
            and escenario["activo"]
        )

    # ==========================
    # HELPERS
    # ==========================

    def _formatear(self, row):
        return {
            "id": row["id"],
            "cliente": {
                "cedula":    row["cliente_cedula"],
                "nombre":    row["cliente_nombre"],
                "telefono":  row["cliente_telefono"],
                "membresia": row["cliente_membresia"]
            },
            "cancha":   row["cancha"],
            "objetivo": row["objetivo"],
            "fecha":    str(row["fecha"]),
            "hora":     row["hora"],
            "estado":   row["estado"]
        }
